from pydantic import BaseModel, ConfigDict

class ServiceCreate(BaseModel):

    name: str
    duration_minutes: int
    price: float

class ServiceResponse(BaseModel):

    id: int
    name: str
    duration_minutes: int
    price: float
    model_config = ConfigDict(from_attributes=True)