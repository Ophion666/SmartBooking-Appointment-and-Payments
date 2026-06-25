from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):

    name: str

    phone: str

class UserResponse(BaseModel):

    id: int
    name: str
    phone: str
    model_config = ConfigDict(from_attributes=True)