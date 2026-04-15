from sqlalchemy import Column, ForeignKey, Integer, String
from app.models import Base


class WorkingHours(Base):
    __tablename__ = "working_hours"
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    day_of_week = Column(Integer)
    break_start = Column(String)
    break_end = Column(String)
    start = Column(String)
    end = Column(String)
