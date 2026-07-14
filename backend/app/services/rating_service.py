from sqlalchemy.orm import Session
from app.schemas.rating import RatingRequestOut, RatingResponse
from app.crud import crud_rating, crud_master
from fastapi import HTTPException
from datetime import datetime

def get_rating_form(db: Session, token:str) -> RatingRequestOut:
    db_rating = crud_rating.get_rating_request_by_token(db, token=token)
    if not db_rating:
        raise HTTPException(status_code=404, detail="Token not found")
    if db_rating.is_used == True:
        raise HTTPException(status_code=400, detail="You already voted")
    if db_rating.expires_at < datetime.now():
        raise HTTPException(status_code=400, detail="You already voted")
    master = crud_master.get_master_by_id(db, master_id=db_rating.master_id)
    
    return RatingRequestOut( master_name = master.name, expires_at = db_rating.expires_at)

def submit_rating(db: Session, token: str, score: int) -> RatingResponse:
    db_rating = crud_rating.get_rating_request_by_token(db, token=token)
    if not db_rating:
        raise HTTPException(status_code=404, detail="Token not found")
    if db_rating.is_used == True:
        raise HTTPException(status_code=400, detail="You already voted")
    if db_rating.expires_at < datetime.now():
        raise HTTPException(status_code=400, detail="Link already end")
    appointment_id = db_rating.appointment_id
    master_id = db_rating.master_id
    save = crud_rating.create_rating(db, appointment_id=appointment_id, master_id=master_id, score=score)
    db_rating.is_used = True
    avg_score, count = crud_rating.get_master_rating_stats(db, master_id=master_id)
    master = crud_master.get_master_by_id(db, master_id=master_id)
    master.rating_avg = avg_score
    master.rating_count = count
    db.commit()
    return save