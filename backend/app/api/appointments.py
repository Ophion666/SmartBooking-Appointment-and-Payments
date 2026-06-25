from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import crud_appointment, crud_service
from app.schemas import appointments
import math
from datetime import timedelta


router = APIRouter(prefix="/appointments", tags=["Appointment"])


@router.post("/appointment", response_model=appointments.AppointmentResponse)
def post_create_appointment(appoint: appointments.AppointmentCreate, db: Session = Depends(get_db)):
    service = crud_service.get_service_by_id(db, service_id=appoint.service_id)

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    slots_needed = math.ceil(service.duration_minutes / 30)
    requested_slots = set()

    for i in range(slots_needed):
        time_str = (appoint.start_datetime + timedelta(minutes=30 * i)).strftime("%H:%M")
        requested_slots.add(time_str)

    target_date = appoint.start_datetime.date()
    existing_appts = crud_appointment.get_appointments_by_master_and_date(db, appoint.master_id, target_date)

    booked_slots = set()

    for existing in existing_appts:
        dur = existing.service.duration_minutes
        count = math.ceil(dur / 30)
        for i in range(count):
            blocked = (existing.start_datetime + timedelta(minutes=30 * i)).strftime("%H:%M")
            booked_slots.add(blocked)

    if requested_slots.intersection(booked_slots):
        raise HTTPException(status_code=400, detail="Time booked")

    return crud_appointment.create_appointment(db=db, appoint=appoint)
