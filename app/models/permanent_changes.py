from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.models import Base

class PermanentChange(Base):
    __tablename__ = "permanent_changes"
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    effective_from = Column(DateTime)
    day_of_week = Column(Integer)
    start = Column(String)
    end = Column(String)
