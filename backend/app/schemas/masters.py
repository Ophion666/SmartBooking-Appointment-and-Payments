from pydantic import BaseModel, ConfigDict

class ServiceShortInfo(BaseModel):
    id: int
    name: str
    price: float
    duration_minutes: int
    model_config = ConfigDict(from_attributes=True)


class MasterCreate(BaseModel):

    name: str
    specialization: str
    phone: str

class MasterResponse(BaseModel):
    
    id: int
    name: str
    specialization: str
    phone: str
    services: list[ServiceShortInfo] = [] 
    model_config = ConfigDict(from_attributes=True)


class MasterShort(BaseModel):
    id: int
    name: str
    rating_avg: float | None = None
    rating_count: int