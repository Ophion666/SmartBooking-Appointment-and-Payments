from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import appointments
from app.services import appointment_service

router = APIRouter(prefix="/appointments", tags=["Appointment"])


@router.post("/appointment", response_model=appointments.AppointmentResponse)
def post_create_appointment(appoint: appointments.AppointmentCreate, db: Session = Depends(get_db)):
    return appointment_service.create_new_appointment(db=db, appoint=appoint)