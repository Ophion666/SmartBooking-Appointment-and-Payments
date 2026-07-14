from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class RatingCreate(BaseModel):
    score: int = Field(ge=1, le=5)


class RatingResponse(BaseModel):
    id: int
    master_id: int
    score: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class RatingRequestOut(BaseModel):
    master_name: str
    expires_at: datetime
    model_config = ConfigDict(from_attributes=True)