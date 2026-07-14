from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import appointments
from app.crud import crud_appointment
from app.services import appointment_service
from app.api.worker import cancel_unpaid_task
from app.models.users import User
from app.services.current_admin import get_current_admin

router = APIRouter(prefix="/appointments", tags=["Appointment"])


@router.post("/appointment", response_model=appointments.AppointmentResponse)
def post_create_appointment(appoint: appointments.AppointmentCreate, db: Session = Depends(get_db)):
    new_appoint = appointment_service.create_new_appointment(db=db, appoint=appoint)
    cancel_unpaid_task.apply_async(args=[new_appoint.id], countdown = 600) 
    return new_appoint

@router.post("/cancel/{appointment_id}")
def cancel_appointment_admin_endpoint(appointment_id: str, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return appointment_service.cancel_appointment_admin(db=db, appointment_id=appointment_id)

@router.get("/appointment/{appointment_id}/details", response_model=appointments.AppointmentDetailsResponse)
def get_appointment_detail_endpoin(appointment_id: int, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return crud_appointment.get_details_appointment(db=db,appointment_id=appointment_id)