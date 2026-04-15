from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt
from app.models import SessionLocal
from app.utils.auth import SECRET_KEY, ALGORITHM
from app.models.doctors import Doctor
from app.models.patients import Patient

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()


def get_current_user(token=Depends(security), db=Depends(get_db)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        print(e)
        raise HTTPException(401)

    if payload["type"] == "Doctor":
        return db.get(Doctor, int(payload["sub"]))
    
    return db.get(Patient, int(payload["sub"]))
