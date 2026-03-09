from fastapi import APIRouter, Depends, status, HTTPException
from app.auth import process_token
from app.models import RFIDScanRequest
from app.tables import AttendanceLog, Device
from fastapi.responses import JSONResponse
from app.db import get_session
from uuid import uuid4
from datetime import datetime, timezone, timedelta
from sqlmodel import select,desc

router = APIRouter(prefix="/iot")


@router.post("/rfid-scan")
def rfid_scan(request: RFIDScanRequest, session=Depends(get_session), token=Depends(process_token)):
    device = session.exec(select(Device).where(Device.device_id == request.device_id)).first()
    query = select(AttendanceLog).order_by(desc(AttendanceLog.scanned_at)).where(Device.device_id == request.device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device Not Found"
        )

    attendance = AttendanceLog(
        event_id=str(uuid4()),
        device_id=request.device_id,
        card_uid=request.card_uid,
        scanned_at=datetime.now(timezone.utc),
    )
    latest_scan = session.exec(query.where(AttendanceLog.card_uid == request.card_uid)).first()
    try:
        scan_again = latest_scan.scanned_at.replace(tzinfo=timezone.utc) + timedelta(hours=20)
        if latest_scan and scan_again > attendance.scanned_at:
            return {"error": "too many requests"}
    except AttributeError:
        pass
    session.add(attendance)
    session.commit()
    session.refresh(attendance)
    return JSONResponse(
        content={"event_id": attendance.event_id, "message": "Attendance Received"},
        status_code=status.HTTP_201_CREATED
    )

