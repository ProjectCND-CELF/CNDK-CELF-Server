from datetime import datetime, timezone
from fastapi import APIRouter, status, Depends
from app.models import DeviceRegisterRequest
from app.tables import Device
from app.auth import process_token
from sqlmodel import select
from fastapi.responses import JSONResponse
from app.db import get_session
router = APIRouter(prefix="/devices")


@router.post("/register", status_code=status.HTTP_200_OK)
def register_device(devicereg: DeviceRegisterRequest, session=Depends(get_session), token=Depends(process_token)):
    device = session.exec(select(Device).where(Device.device_id == devicereg.device_id)).first()
    if device:
        device.firmware_version = devicereg.firmware_version
        session.commit()
        session.refresh(device)
        return JSONResponse(
            content={"Notice": "Updated Firmware"},
            status_code=status.HTTP_200_OK
        )

    new_device_object = Device(
        device_id=devicereg.device_id,
        firmware_version=devicereg.firmware_version,
        registered_at=datetime.now(timezone.utc)
    )
    session.add(new_device_object)
    session.commit()
    session.refresh(new_device_object)
    return JSONResponse(
        content={"Notice": "Device Added"},
        status_code=status.HTTP_201_CREATED
    )


@router.get("/")
def get_devices(session=Depends(get_session), token=Depends(process_token)):
    devices = session.exec(select(Device)).all()
    return devices
