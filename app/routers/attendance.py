from fastapi import APIRouter, Depends
from app.auth import process_token
from app.db import get_session
from app.tables import AttendanceLog
from sqlmodel import select, desc

router = APIRouter(prefix="/attendance")


@router.get("/")
def get_logs(limit: int = None, device_id: str = None, session=Depends(get_session), token=Depends(process_token)):
    query = select(AttendanceLog).order_by(desc(AttendanceLog.scanned_at))
    if device_id:
        query = query.where(AttendanceLog.device_id == device_id)
    if limit:
        query = query.limit(limit)
    results_lists = session.exec(query).all()
    return {"Results": results_lists}


