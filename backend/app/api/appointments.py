from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import appointments
from app.services import appointment_service
from app.api.worker import cancel_unpaid_task

router = APIRouter(prefix="/appointments", tags=["Appointment"])


@router.post("/appointment", response_model=appointments.AppointmentResponse)
def post_create_appointment(appoint: appointments.AppointmentCreate, db: Session = Depends(get_db)):
    new_appoint = appointment_service.create_new_appointment(db=db, appoint=appoint)
    cancel_unpaid_task.apply_async(args=[new_appoint.id], PAYMENT_TIMEOUT_SECONDS = 600) 
    return new_appoint

@router.post("/cancel/{appointment_id}")
def cancel_appointment_admin_endpoint(appointment_id: str, db: Session = Depends(get_db)):
    return appointment_service.cancel_appointment_admin(db=db, appointment_id=appointment_id)