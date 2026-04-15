from fastapi import APIRouter
from app.routers.v1.auth import router as auth
from app.routers.v1.appointments import router as appointments
from app.routers.v1.working_hours import router as working_hours


router = APIRouter(prefix="/v1")

router.include_router(auth)
router.include_router(appointments)
router.include_router(working_hours)
