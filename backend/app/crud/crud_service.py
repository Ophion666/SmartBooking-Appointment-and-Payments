from sqlalchemy.orm import Session
from app.models.services import Service
from app.schemas.services import ServiceCreate

def create_service(db: Session, service: ServiceCreate):
    db_service = Service(name = service.name, duration_minutes = service.duration_minutes, price = service.price)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def get_service_by_name(db: Session, name: int):
    return db.query(Service).filter(Service.name == name).first()

def get_all_services(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Service).filter(Service.is_active == True).offset(skip).limit(limit).all()

def get_service_by_id(db: Session, service_id: int):
    return db.query(Service).filter(Service.id == service_id).first()

def delete_service(db: Session, service_id: int):
    db_service = get_service_by_id(db, service_id=service_id)
    if db_service:
        db_service.is_active = False
        db.commit()
        db.refresh(db_service)
    return db_service

def activate_service(db: Session, service_id: int):
    db_service = get_service_by_id(db, service_id=service_id)
    if db_service:
        db_service.is_active = True
        db.commit()
        db.refresh(db_service)
    return db_service