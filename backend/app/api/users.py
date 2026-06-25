from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_user
from app.schemas import users
from app.db.session import get_db


router = APIRouter(prefix="/user", tags=["Users"])

@router.post("/register", response_model=users.UserResponse)
def post_create_user(user: users.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_phone(db, phone=user.phone)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud_user.create_user(db = db, user=user)

@router.get("/users", response_model= list[users.UserResponse])
def get_users (db: Session = Depends(get_db)):
    return crud_user.get_all_users(db = db)