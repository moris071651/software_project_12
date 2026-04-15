from datetime import time
from app.models.working_hours import WorkingHours
from app.models.temp_changes import TempChange
from app.models.permanent_changes import PermanentChange


def str_to_time(t: str) -> time:
    h, m = map(int, t.split(":"))
    return time(hour=h, minute=m)


def check_range(start, end, s, e):
    return str_to_time(start) <= s.time() and e.time() <= str_to_time(end)


def overlaps_break(wh, s, e):
    if not wh.break_start:
        return False
    b1 = str_to_time(wh.break_start)
    b2 = str_to_time(wh.break_end)
    return not (e.time() <= b1 or s.time() >= b2)


def is_within_working_hours(db, doctor_id, start, end):
    day = start.weekday()

    temp = db.query(TempChange).filter(
        TempChange.doctor_id == doctor_id,
        TempChange.start_date <= start,
        TempChange.end_date >= end
    ).first()

    if temp:
        return check_range(temp.start, temp.end, start, end)

    perm = db.query(PermanentChange).filter(
        PermanentChange.doctor_id == doctor_id,
        PermanentChange.day_of_week == day,
        PermanentChange.effective_from <= start
    ).order_by(PermanentChange.effective_from.desc()).first()

    if perm:
        return check_range(perm.start, perm.end, start, end)

    wh = db.query(WorkingHours).filter(
        WorkingHours.doctor_id == doctor_id,
        WorkingHours.day_of_week == day
    ).first()

    if not wh:
        return False

    if not check_range(wh.start, wh.end, start, end):
        return False

    if overlaps_break(wh, start, end):
        return False

    return True
