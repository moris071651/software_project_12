from fastapi import APIRouter, Depends
from app.utils.dep import get_db, get_current_user
from app.schemas.appointment import AppointmentCreate
from app.services.appointments import create_appointment, cancel_appointment, list_my_appointments

router = APIRouter(prefix="/appointments")


@router.post("/")
def create(data: AppointmentCreate, db=Depends(get_db), user=Depends(get_current_user)):
    return create_appointment(db, data, user)


@router.delete("/{id}")
def cancel(id: int, db=Depends(get_db), user=Depends(get_current_user)):
    return cancel_appointment(db, id, user)


@router.get("/me")
def my_appointments(db=Depends(get_db), user=Depends(get_current_user)):
    return list_my_appointments(db, user)
