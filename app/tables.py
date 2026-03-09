from sqlmodel import SQLModel, Field
from datetime import datetime


class Device(SQLModel, table=True):
    device_id: str = Field(default=None, primary_key=True)
    firmware_version: str
    registered_at: datetime


class AttendanceLog(SQLModel, table=True):
    event_id: str = Field(default=None, primary_key=True)
    device_id: str
    card_uid: str
    scanned_at: datetime
