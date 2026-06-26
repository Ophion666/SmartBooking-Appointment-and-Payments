from sqlalchemy.orm import Session
from app.models.appointments import Appointment
from app.schemas.appointments import AppointmentCreate, AppointmentStatus
from datetime import date
from sqlalchemy import cast, Date



def get_appointment_by_id(db: Session, appointment_id: int):
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


def get_all_appointments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Appointment).offset(skip).limit(limit).all()


def get_appointments_by_master_and_date(db: Session, master_id: int, target_date: date):
    return db.query(Appointment).filter(
        Appointment.master_id == master_id,
        cast(Appointment.start_datetime, Date) == target_date,
        Appointment.status != AppointmentStatus.cancelled 
    ).all()


def get_appoint_by_token(db: Session, token: str):
    return db.query(Appointment).filter(Appointment.cancel_token == token).first()