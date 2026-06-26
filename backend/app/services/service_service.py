from sqlalchemy.orm import Session
from app.crud import crud_service
from app.services.current_admin import get_current_admin
from app.models.users import User
from fastapi import HTTPException


def delete_services(service_id: int, db: Session, current_admin: User):

    delete_service = crud_service.delete_service(db, service_id=service_id)

    if not delete_service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    return {"message": "Success"}