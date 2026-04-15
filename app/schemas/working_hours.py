from pydantic import BaseModel


class WorkingHoursCreate(BaseModel):
    day: int
    start: str
    end: str
    break_start: str | None = None
    break_end: str | None = None
