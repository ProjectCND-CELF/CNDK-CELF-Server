from pydantic import BaseModel


class DeviceRegisterRequest(BaseModel):
    device_id: str
    firmware_version: str


class RFIDScanRequest(BaseModel):
    device_id: str
    card_uid: str





