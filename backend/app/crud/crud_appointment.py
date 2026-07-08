from sqlalchemy.orm import Session, joinedload
from app.models.appointments import Appointment
from app.schemas.appointments import AppointmentStatus
from datetime import date
from datetime import datetime, time, timedelta
from sqlalchemy import asc


def get_appointment_by_id(db: Session, appointment_id: int):
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


def get_all_appointments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Appointment).offset(skip).limit(limit).all()


def get_appointments_by_master_and_date(db: Session, master_id: int, target_date: date):
    start = datetime.combine(target_date, time.min)
    end = start + timedelta(days=1)

    return db.query(Appointment).filter(
        Appointment.master_id == master_id,
        Appointment.start_datetime >= start,
        Appointment.start_datetime < end,
        Appointment.status != AppointmentStatus.cancelled,
    ).all()


def get_appoint_by_token(db: Session, token: str):
    return db.query(Appointment).filter(Appointment.cancel_token == token).first()


def get_master_appointments(db: Session, master_id: int):
    return db.query(Appointment).filter(
        Appointment.master_id == master_id
    ).order_by(
        asc(Appointment.start_datetime)
    ).all()


def get_user_appointment(db: Session, user_id: int):
    return db.query(Appointment).filter(Appointment.user_id == user_id).all()

def get_details_appointment(db: Session, appointment_id: int):
    return db.query(Appointment).filter(Appointment.id == appointment_id).options(
        joinedload(Appointment.user),
        joinedload(Appointment.master),
        joinedload(Appointment.service),
    ).first()