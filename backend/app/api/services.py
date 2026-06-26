from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import services
from app.services import service_service
from app.crud import crud_service
from app.models.users import User
from app.services.current_admin import get_current_admin

router = APIRouter(prefix="/service", tags=["Services"])

@router.post("/create_service", response_model=services.ServiceResponse)
def post_create_service(service: services.ServiceCreate, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    db_service = crud_service.get_service_by_name(db, name = service.name)
    if db_service:
        raise HTTPException(status_code=400, detail="Service already registered")
    return crud_service.create_service(db=db, service=service)

@router.get("/services", response_model=list[services.ServiceResponse])
def get_services (db: Session = Depends(get_db)):
    return crud_service.get_all_services(db=db)

@router.delete("/{service_id}")
def delete_service_endpoint(service_id: int, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return service_service.delete_services(db=db, service_id=service_id, current_admin=current_admin)