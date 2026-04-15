from datetime import datetime
from pydantic import BaseModel


class AppointmentCreate(BaseModel):
    start: datetime
    end: datetime
    doctor_id: int
    

class AppointmentResponse(BaseModel):
    id: int
    start: datetime
    end: datetime

    class Config:
        from_attributes = True
