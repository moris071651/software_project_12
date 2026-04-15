from datetime import datetime, timedelta, UTC
import os
from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto",
)

def hash_password(p):
    return pwd_context.hash(p)


def verify_password(p, h):
    return pwd_context.verify(p, h)


def create_token(data: dict):
    data["exp"] = datetime.now(UTC) + timedelta(hours=1)
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
