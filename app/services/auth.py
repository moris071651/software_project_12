from fastapi import HTTPException
from app.models.doctors import Doctor
from app.models.patients import Patient
from app.schemas.auth import UserOut
from app.utils.auth import hash_password, verify_password, create_token

def register_doctor(db, data):
    existing = db.query(Doctor).filter_by(email=data.email).first() or \
           db.query(Patient).filter_by(email=data.email).first()

    if existing:
        raise HTTPException(400, "Email already exists")
    
    d = Doctor(name=data.name, email=data.email, address=data.address, password=hash_password(data.password))
    db.add(d); db.commit(); db.refresh(d)
    
    return UserOut.model_validate(d)


def register_patient(db, data):
    existing = db.query(Doctor).filter_by(email=data.email).first() or \
       db.query(Patient).filter_by(email=data.email).first()

    if existing:
        raise HTTPException(400, "Email already exists")
    
    existing_doc = db.query(Doctor).filter_by(id=data.doctor_id).first()

    if not existing_doc:
        raise HTTPException(400, "Doctor does not exists")

    p = Patient(name=data.name, email=data.email, phone=data.phone, password=hash_password(data.password), doctor_id=data.doctor_id)
    db.add(p); db.commit(); db.refresh(p)

    return UserOut.model_validate(p)


def login(db, data):
    user = db.query(Doctor).filter_by(email=data.email).first() or \
           db.query(Patient).filter_by(email=data.email).first()

    if not user or not verify_password(data.password, user.password):
        return None

    return create_token({"sub": str(user.id), "type": user.__class__.__name__})
