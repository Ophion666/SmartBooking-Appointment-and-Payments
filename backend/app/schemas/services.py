from pydantic import BaseModel, ConfigDict

class MasterShortInfo(BaseModel):
    id: int
    name: str
    phone: str
    specialization: str
    model_config = ConfigDict(from_attributes=True)

class ServiceCreate(BaseModel):

    name: str
    duration_minutes: int
    price: float

class ServiceResponse(BaseModel):

    id: int
    name: str
    duration_minutes: int
    price: float
    masters: list[MasterShortInfo] = []
    model_config = ConfigDict(from_attributes=True)

class ServiceShort(BaseModel):
    id: int
    name: str
    price: float
    duration_minutes: int