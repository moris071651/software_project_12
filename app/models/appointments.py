from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from app.models import Base


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    start = Column(DateTime)
    end = Column(DateTime)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))
    cancelled = Column(Boolean, default=False)