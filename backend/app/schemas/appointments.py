from enum import Enum
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class AppointmentStatus(str, Enum):
    pending_payment = "pending_payment"
    confirmed = "confirmed"
    cancelled = "cancelled"

class AppointmentCreate(BaseModel):

    user_id: int
    master_id: int
    service_id: int
    start_datetime: datetime
    status: AppointmentStatus

class AppointmentResponse(BaseModel):

    id: int
    user_id: int
    master_id: int
    service_id: int
    start_datetime: datetime
    status: AppointmentStatus

    model_config = ConfigDict(from_attributes=True)