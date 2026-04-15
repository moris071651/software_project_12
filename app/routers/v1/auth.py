from fastapi import APIRouter, Depends, HTTPException
from app.schemas.auth import Login, RegisterDoctor, RegisterPatient
from app.services.auth import login, register_doctor, register_patient
from app.utils.dep import get_db

router = APIRouter(prefix="/auth")


@router.post("/register/doctor")
def reg_doc(data: RegisterDoctor, db=Depends(get_db)):
    return register_doctor(db, data)


@router.post("/register/patient")
def reg_pat(data: RegisterPatient, db=Depends(get_db)):
    return register_patient(db, data)


@router.post("/login")
def log(data: Login, db=Depends(get_db)):
    token = login(db, data)
    if not token:
        raise HTTPException(401)
    
    return {"token": token}
