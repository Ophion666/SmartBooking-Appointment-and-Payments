from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import appointments
from app.services import appointment_service

router = APIRouter(prefix="/appointments", tags=["Appointment"])


@router.post("/appointment", response_model=appointments.AppointmentResponse)
def post_create_appointment(appoint: appointments.AppointmentCreate,background_task: BackgroundTasks, db: Session = Depends(get_db)):
    new_appoint = appointment_service.create_new_appointment(db=db, appoint=appoint)

    background_task.add_task(
        appointment_service.cancel_unpaid_appointment_task,appointment_id = new_appoint.id
    )

    return new_appoint

@router.post("/cancel/{appointment_id}")
def cancel_appointment_admin_endpoint(appointment_id: str, db: Session = Depends(get_db)):
    return appointment_service.cancel_appointment_admin(db=db, appointment_id=appointment_id)