import os
from celery import Celery
from dotenv import load_dotenv
from app.services.telegram_service import send_telegram_message
from app.db.session import SessionLocal
from app.models.appointments import Appointment, AppointmentStatus
from app.crud import crud_rating, crud_appointment

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

celery_app = Celery(
    "smart_booking",
    broker=REDIS_URL,
    backend=REDIS_URL
)


@celery_app.task(name="send_telegrame_notification")
def send_telegram_task (text: str):
    print(f"[CELERY] Work above message in tg")
    send_telegram_message(text)
    return ("Success")


@celery_app.task(name="cancel_unpaid_appointment")
def cancel_unpaid_task(appointment_id: int):
    db = SessionLocal()

    try:

        appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()

        if appt and appt.status == AppointmentStatus.pending_payment:
            appt.status = AppointmentStatus.cancelled
            db.commit()
            text = (
                f"<b>TIMEOUT OR PAYMENT AFTER TIMEOUT</b>\n"
                f"appointment #{appointment_id} cancelled, payment refunded"
            )
            send_telegram_task.delay(text)

    finally:
        db.close()



@celery_app.task(name="send_rating_request")
def send_rating_request_task(appointment_id: int):
    db = SessionLocal()

    try:


        appt = crud_appointment.get_appointment_by_id(db, appointment_id)

        if not appt:
            return
        
        existing = crud_rating.get_rating_request_by_appointment(db, appointment_id)

        if existing:
            return

        rating_request = crud_rating.create_rating_request(db, appointment_id, appt.master_id)
        token = rating_request.token
        link = f"http://localhost:8000/rate/{token}"
        text = (
            f"<b>Rating barber</b>\n"
            f"{link}"
        )
        send_telegram_task.delay(text)
    finally:
        db.close()
