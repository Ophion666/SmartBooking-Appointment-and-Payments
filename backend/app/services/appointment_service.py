import math
from datetime import timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_appointment, crud_service, crud_user, crud_master
from app.schemas.appointments import AppointmentCreate, AppointmentStatus
from app.schemas.users import UserCreate
from app.db.session import SessionLocal
from app.models.appointments import Appointment
import stripe
from app.api.worker import send_telegram_task
import asyncio
from typing import Dict

def create_new_appointment(db: Session, appoint: AppointmentCreate):

    user = crud_user.get_user_by_phone(db, phone = appoint.user_phone)
    if not user:
        new_user_data = UserCreate(name= appoint.user_name, phone= appoint.user_phone)
        user = crud_user.create_user(db, user=new_user_data)

    user_id = user.id

    service = crud_service.get_service_by_id(db, service_id=appoint.service_id)

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    master = crud_master.get_master_by_id(db, master_id= appoint.master_id)

    if master.is_active == False:
        raise HTTPException(status_code=404, detail="Master not found")

    if not service in master.services:
        raise HTTPException(status_code=400, detail="Mater doesn't do it")

    
    if service.is_active == False:
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
    
    from app.models.appointments import Appointment

    db_appoint = Appointment(
        user_id = user_id,
        master_id = appoint.master_id,
        service_id = appoint.service_id,
        start_datetime = appoint.start_datetime,
        status = AppointmentStatus.pending_payment
    )

    db.add(db_appoint)
    db.commit()
    db.refresh(db_appoint)

    return db_appoint


def cancel_appointment(db: Session, token: str):
    found_appoint = crud_appointment.get_appoint_by_token(db, token=token)

    if not found_appoint:
        raise HTTPException(404, "Invalid token or appointment not found")
    
    if found_appoint.status == "canceled":
        raise HTTPException(400, "Appointment already cancel")
    
    #active_timers operate only in the memory of a single process.
    if found_appoint.id in active_timers:
        active_timers[found_appoint.id].set()
    
    if found_appoint.status == AppointmentStatus.confirmed and found_appoint.stripe_payment_id:
        try:
            stripe.Refund.create(payment_intent=found_appoint.stripe_payment_id)
            print(f"Refund payment for appointment {found_appoint.id} success")
        except Exception as e:
            print(f"Error of refund: {e}")
    
    found_appoint.status = AppointmentStatus.cancelled

    db.commit()
    db.refresh(found_appoint)

    text = f"<b>Canceling appointment</b>\n User canceled appointment {found_appoint.id} by url"
    send_telegram_task.delay(text)

    return found_appoint

def cancel_appointment_admin(db: Session, appointment_id: str):
    found_appoint = crud_appointment.get_appointment_by_id(db, appointment_id=appointment_id)

    if not found_appoint:
        raise HTTPException(404, "Invalid token or appointment not found")
    
    if found_appoint.status == "canceled":
        raise HTTPException(400, "Appointment already cancel")
    
    found_appoint.status = AppointmentStatus.cancelled

    db.commit()
    db.refresh(found_appoint)
    return found_appoint

active_timers: Dict[int, asyncio.Event] = {}

async def cancel_unpaid_appointment_task(appointment_id: int):
    stop_event = asyncio.Event()
    active_timers[appointment_id] = stop_event

    try:

        await asyncio.wait_for(stop_event.wait(), timeout=600)

        print(f"[Timer] Payment success/canceled. Timer for {appointment_id} stopped")

    except asyncio.TimeoutError:

        db = SessionLocal()

        try:

            appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()

            if appt and appt.status == AppointmentStatus.pending_payment:
                appt.status = AppointmentStatus.cancelled
                db.commit()
                text = (
                    f"<b>TIMEOUT OR PAYMENT AFTER TIMEOUT</b>\n"
                    f"appointment #{appointment_id} canceled, payment refunded"
                )
                send_telegram_task.delay(text)

        finally:
            db.close()

    finally:
        active_timers.pop(appointment_id, None)