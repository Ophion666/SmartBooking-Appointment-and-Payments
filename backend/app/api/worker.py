import os
from celery import Celery
from dotenv import load_dotenv
from app.services.telegram_service import send_telegram_message

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