from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import rating_service
from app.schemas import rating

router = APIRouter(prefix="/rating", tags=["Rating"])

@router.get("/rate/{token}", response_model=rating.RatingRequestOut)
def get_rating_form_endpoint(token:str, db: Session = Depends(get_db)):
    return rating_service.get_rating_form(db=db, token=token)

@router.post("/rate/{token}", response_model=rating.RatingResponse)
def submit_rating(token: str, payload: rating.RatingCreate, db: Session = Depends(get_db)):
    return rating_service.submit_rating(db, token, payload.score)