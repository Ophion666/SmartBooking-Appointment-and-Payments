
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from datetime import date
from app.services import booking_service, appointment_service

router = APIRouter(prefix="/booking", tags=["Booking"])


@router.get("/{master_id}/avaible-slots")
def available_slots(master_id: int,service_id: int , target_date: date, db: Session = Depends(get_db)):
    return booking_service.get_available_slots(db = db, master_id=master_id, service_id=service_id, target_date=target_date)
    

    

@router.post("/cancel/{token}")
def cancel_appointment_endpoint(token: str, db: Session = Depends(get_db)):
    return appointment_service.cancel_appointment(db=db, token=token)


