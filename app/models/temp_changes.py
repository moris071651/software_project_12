from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.models import Base

class TempChange(Base):
    __tablename__ = "temp_changes"
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    start = Column(String)
    end = Column(String)
    