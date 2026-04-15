from sqlalchemy import Column, ForeignKey, Integer, String
from app.models import Base


class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    password = Column(String)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
