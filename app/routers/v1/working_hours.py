from fastapi import APIRouter, Depends
from app.schemas.working_hours import WorkingHoursCreate
from app.services.working_hours import create_base_working_hours, create_permanent_change, create_temp_change
from app.utils.dep import get_db, get_current_user


router = APIRouter(prefix="/working-hours")


@router.post("/")
def base(data: WorkingHoursCreate, db=Depends(get_db), user=Depends(get_current_user)):
    return create_base_working_hours(db, data.model_dump(), user)


@router.post("/temp")
def temp(data: WorkingHoursCreate, db=Depends(get_db), user=Depends(get_current_user)):
    return create_temp_change(db, data.model_dump(), user)


@router.post("/permanent")
def perm(data: WorkingHoursCreate, db=Depends(get_db), user=Depends(get_current_user)):
    return create_permanent_change(db, data.model_dump(), user)
