from sqlalchemy.orm import Session
from app.models.masters import Master
from app.schemas.masters import MasterCreate

def create_master(db: Session, master: MasterCreate):
    db_master = Master(name = master.name, specialization = master.specialization, phone = master.phone)
    db.add(db_master)
    db.commit()
    db.refresh(db_master)
    return db_master

def get_master_by_id(db: Session, master_id: int):
    return db.query(Master).filter(Master.id == master_id).first()

def get_master_by_phone(db: Session, phone: str):
    return db.query(Master).filter(Master.phone == phone).first()

def get_all_masters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Master).filter(Master.is_active == True).offset(skip).limit(limit).all()

def deactivate_master(db: Session, master_id: int):
    db_master = get_master_by_id(db, master_id=master_id)
    if db_master:
        db_master.is_active = False
        db.commit()
        db.refresh(db_master)
    return db_master

def activate_master(db: Session, master_id: int):
    db_master = get_master_by_id(db, master_id=master_id)
    if db_master:
        db_master.is_active = True
        db.commit()
        db.refresh(db_master)
    return db_master