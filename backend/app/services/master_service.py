from app.crud import crud_service, crud_master
from sqlalchemy.orm import Session
from fastapi import HTTPException
import json
from app.core.redis_client import redis_client
from app.schemas.masters import MasterResponse

MASTERS_CACHE_KEY = "masters:all"
MASTERS_CACHE_TTL = 3600

def get_masters_cached(db: Session):
    key = redis_client.get(MASTERS_CACHE_KEY)
    if key:
        return json.loads(key)
    key_orm = crud_master.get_all_masters(db)
    resault = [MasterResponse.model_validate(i).model_dump() for i in key_orm]

    redis_client.set(MASTERS_CACHE_KEY, json.dumps(resault), ex=MASTERS_CACHE_TTL)

    return resault

def invalidate_masters_cache():
    return redis_client.delete(MASTERS_CACHE_KEY)

def assign_service_to_master(master_id: int, service_id: int, db: Session):

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
    invalidate_masters_cache()

    return {"message": f"Service '{service.name}' added to Master '{master.name}'"}


def deactivate_masters(master_id: int, db: Session):
    deactivate_master = crud_master.deactivate_master(db, master_id=master_id)

    if not deactivate_master:
        raise HTTPException(status_code=404, detail="Master not found")

    invalidate_masters_cache()
    
    return {"message": "Success"}

def activate_masters(master_id: int, db: Session):
    activate_master = crud_master.activate_master(db, master_id=master_id)

    if not activate_master:
        raise HTTPException(status_code=404, detail="Master not found")

    invalidate_masters_cache()
    
    return {"message": "Success"}

