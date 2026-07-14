from sqlalchemy.orm import Session
from app.models.ratings import Rating
from app.models.rating_request import RatingRequest
from sqlalchemy.sql import func
from datetime import datetime, timedelta, timezone

def get_rating_request_by_appointment(db: Session, appointment_id: int):
    return db.query(RatingRequest).filter(RatingRequest.appointment_id == appointment_id).first()


def get_rating_request_by_token(db: Session, token: str):
    return db.query(RatingRequest).filter(RatingRequest.token == token).first()

def create_rating(db: Session, appointment_id: int, master_id: int, score:int):
    db_rating = Rating(appointment_id = appointment_id, master_id = master_id, score = score)
    db.add(db_rating)
    db.flush()
    db.refresh(db_rating)
    return db_rating

def create_rating_request(db: Session, appointment_id: int, master_id: int, ttl_hours=72):
    db_rating_request = RatingRequest(expires_at = datetime.now(timezone.utc) + timedelta(hours=ttl_hours), appointment_id = appointment_id, master_id = master_id)
    db.add(db_rating_request)
    db.commit()
    db.refresh(db_rating_request)
    return db_rating_request

def get_master_rating_stats(db: Session, master_id: int):
    return db.query(
        func.avg(Rating.score), func.count(Rating.id)
    ).filter(Rating.master_id == master_id).one()