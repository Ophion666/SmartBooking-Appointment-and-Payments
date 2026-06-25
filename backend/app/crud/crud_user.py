from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.users import UserCreate

def create_user(db: Session, user: UserCreate):
    db_user = User(name = user.name, phone = user.phone)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return (db_user)

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_phone(db: Session, phone: str):
    return db.query(User).filter(User.phone == phone).first()

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()