from pydantic import BaseModel, ConfigDict


class MasterCreate(BaseModel):

    name: str
    specialization: str
    phone: str

class MasterResponse(BaseModel):
    
    id: int
    name: str
    specialization: str
    phone: str

    model_config = ConfigDict(from_attributes=True)