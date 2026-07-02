from jose import jwt, JWTError
from app.core.security import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer
from fastapi import  Depends, HTTPException, status
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.crud import crud_user
from app.models.users import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")



def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Error, incorrect person",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        

    except JWTError:

        raise credentials_exception
    

    user = crud_user.get_user_by_id(db, user_id=int(user_id))
    if user is None:
        raise credentials_exception

    return user


def get_current_admin(current_user: User = Depends(get_current_user)):

    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You don`t have an administration roots")
    
    return current_user