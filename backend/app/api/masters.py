from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import masters
from app.crud import crud_master
from app.models.users import User
from app.services.current_admin import get_current_admin


router = APIRouter(prefix="/master", tags=["Masters"])

@router.post("/master_create", response_model=masters.MasterResponse)
def post_create_master(master: masters.MasterCreate, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    db_master = crud_master.get_master_by_phone(db, phone = master.phone)
    if db_master:
        raise HTTPException(status_code=400, detail="Master already registered")
    return crud_master.create_master(db=db, master=master)

@router.get("/masters", response_model=list[masters.MasterResponse])
def get_masters (db: Session = Depends(get_db)):
    return crud_master.get_all_masters(db = db)