from fastapi import FastAPI
from app.routers.attendance import router as attendance_router
from app.routers.devices import router as devices_router
from app.routers.iot import router as iot_router
from app.db import init_db
from app.tables import Device, AttendanceLog

app = FastAPI()
init_db()

app.include_router(attendance_router)
app.include_router(devices_router)
app.include_router(iot_router)

