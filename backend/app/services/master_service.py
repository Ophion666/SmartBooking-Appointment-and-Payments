from app.crud import crud_service, crud_master
from sqlalchemy.orm import Session
from app.services.current_admin import get_current_admin
from app.models.users import User
from fastapi import HTTPException

def assign_service_to_master(master_id: int, service_id: int, db: Session, current_admin: User = get_current_admin):

    master = crud_master.get_master_by_id(db, master_id = master_id)
    if not master: 
        raise HTTPException(status_code=404, detail="Master not found")
    
    service = crud_service.get_service_by_id(db, service_id=service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    if service in master.services:
        raise HTTPException(status_code=400, detail="Master already provides this service")
    
    master.services.append(service)

    db.commit()


    return {"message": f"Service '{service.name}' added to Master '{master.name}'"}


def deactivate_masters(master_id: int, db: Session, current_admin: User):
    deactivate_master = crud_master.deactivate_master(db, master_id=master_id)

    if not deactivate_master:
        raise HTTPException(status_code=404, detail="Master not found")
    
    return {"message": "Success"}

def activate_masters(master_id: int, db: Session, current_admin: User):
    activate_master = crud_master.activate_master(db, master_id=master_id)

    if not activate_master:
        raise HTTPException(status_code=404, detail="Master not found")
    
    return {"message": "Success"}

