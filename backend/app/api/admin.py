from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.services import admin_service
from app.services.current_admin import get_current_admin
from app.models.users import User


router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/login")
def login_admin_endpoint(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return admin_service.login_admin(db=db, form_data=form_data)
