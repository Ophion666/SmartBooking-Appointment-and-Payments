from sqlalchemy.orm import Session
from app.crud import crud_service
from fastapi import HTTPException
from app.schemas.services import ServiceResponse
import json
from app.core.redis_client import redis_client

SERVICES_CACHE_KEY = "services:all"
SERVICES_CACHE_TTL = 3600

def get_services_cached(db: Session):
    key = redis_client.get(SERVICES_CACHE_KEY)
    if key:
        return json.loads(key)
    key_orm = crud_service.get_all_services(db)
    resault = [ServiceResponse.model_validate(i).model_dump() for i in key_orm]

    redis_client.set(SERVICES_CACHE_KEY, json.dumps(resault), ex=SERVICES_CACHE_TTL)

    return resault

def invalidate_services_cache():
    return redis_client.delete(SERVICES_CACHE_KEY)


def delete_services(service_id: int, db: Session):

    delete_service = crud_service.delete_service(db, service_id=service_id)

    if not delete_service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    invalidate_services_cache()
    
    return {"message": "Success"}


def activate_services(service_id: int, db: Session):

    activate_services = crud_service.activate_service(db, service_id=service_id)

    if not activate_services:
        raise HTTPException(status_code=404, detail="Service not found")

    invalidate_services_cache()
    
    return {"message": "Success"}