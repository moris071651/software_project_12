from datetime import datetime, timedelta
from fastapi import HTTPException
from app.models.appointments import Appointment
from app.models.patients import Patient
from app.schemas.appointment import AppointmentResponse
from app.utils.date import is_within_working_hours

def create_appointment(db, data, user):
    if user.__class__.__name__ != "Patient":
        raise HTTPException(403)
    
    if data.end <= data.start:
        raise HTTPException(400, "Invalid time range")

    if data.start < datetime.utcnow() + timedelta(hours=24):
        raise HTTPException(400, "Must be 24h before")

    patient = db.get(Patient, user.id)

    if not patient.doctor_id:
        raise HTTPException(400, "Patient has no assigned doctor")

    if patient.doctor_id != data.doctor_id:
        raise HTTPException(400, "Not your doctor")
    
    if not is_within_working_hours(db, data.doctor_id, data.start, data.end):
        raise HTTPException(400, "Outside working hours")

    overlap = db.query(Appointment).filter(
        Appointment.doctor_id == data.doctor_id,
        Appointment.start < data.end,
        Appointment.end > data.start,
        Appointment.cancelled == False
    ).first()

    if overlap:
        raise HTTPException(400, "Overlap")

    appt = Appointment(
        start=data.start,
        end=data.end,
        doctor_id=data.doctor_id,
        patient_id=user.id
    )

    db.add(appt)
    db.commit()
    db.refresh(appt)

    return appt


def cancel_appointment(db, appt_id, user):
    appt = db.get(Appointment, appt_id)

    if not appt:
        raise HTTPException(404)

    if user.id not in [appt.patient_id, appt.doctor_id]:
        raise HTTPException(403)
    
    if datetime.utcnow() > appt.start - timedelta(hours=12):
        raise HTTPException(400, "Too late to cancel")

    appt.cancelled = True
    db.commit()

    return {"status": "cancelled"}


def list_my_appointments(db, user):
    return [AppointmentResponse.model_validate(x) for x in db.query(Appointment).filter(
        (Appointment.patient_id == user.id) |
        (Appointment.doctor_id == user.id)
    ).all()]