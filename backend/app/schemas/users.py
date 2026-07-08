from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):

    name: str

    phone: str

class UserResponse(BaseModel):

    id: int
    name: str
    phone: str
    model_config = ConfigDict(from_attributes=True)



class Token(BaseModel):
    access_token: str
    token_type: str

class UserShort(BaseModel):
    id: int
    name: str