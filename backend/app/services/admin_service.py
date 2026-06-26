from fastapi import  HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.crud import crud_user
from app.core.security import verify_password, create_access_token
from app.schemas.users import Token


def login_admin(form_data: OAuth2PasswordRequestForm, db: Session):

    user = crud_user.get_user_by_phone(db, phone=form_data.username)

    if not user or not user.is_admin:
        raise HTTPException(status_code=401, detail="Incorrect data")
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}