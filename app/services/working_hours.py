from fastapi import HTTPException
from datetime import datetime, timedelta
from app.models.working_hours import WorkingHours
from app.models.permanent_changes import PermanentChange
from app.models.temp_changes import TempChange


def create_base_working_hours(db, data, user):
    if user.__class__.__name__ != "Doctor":
        raise HTTPException(403, "Only doctors can set working hours")
    
    if data["start"] >= data["end"]:
        raise HTTPException(status_code=400, detail="Invalid range")

    wh = WorkingHours(
        doctor_id=user.id,
        day_of_week=data["day"],
        start=data["start"],
        end=data["end"],
        break_start=data.get("break_start"),
        break_end=data.get("break_end")
    )

    db.add(wh)
    db.commit()
    db.refresh(wh)

    return wh


def create_temp_change(db, data, user):
    if user.__class__.__name__ != "Doctor":
        raise HTTPException(403)

    existing = db.query(TempChange).filter(
        TempChange.doctor_id == user.id
    ).first()

    if existing:
        raise HTTPException(400, "Only one temporary change allowed")
    
    if data["start"] >= data["end"]:
        raise HTTPException(status_code=400, detail="Invalid range")


    temp = TempChange(
        doctor_id=user.id,
        start_date=data["start_date"],
        end_date=data["end_date"],
        start=data["start"],
        end=data["end"]
    )

    db.add(temp)
    db.commit()
    db.refresh(temp)

    return temp


def create_permanent_change(db, data, user):
    if user.__class__.__name__ != "Doctor":
        raise HTTPException(403)

    if data["effective_from"] < datetime.utcnow() + timedelta(days=7):
        raise HTTPException(400, "Must be at least 1 week in future")
    
    if data["start"] >= data["end"]:
        raise HTTPException(status_code=400, detail="Invalid range")

    perm = PermanentChange(
        doctor_id=user.id,
        day_of_week=data["day"],
        effective_from=data["effective_from"],
        start=data["start"],
        end=data["end"]
    )

    db.add(perm)
    db.commit()
    db.refresh(perm)

    return perm
