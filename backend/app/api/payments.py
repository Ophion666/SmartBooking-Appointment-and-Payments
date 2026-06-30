from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import payments_service
router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/create-checkout-session/{appointment_id}")
def create_checkout_session_endpoint(appointment_id: int, db: Session = Depends(get_db)):
    return payments_service.create_checkout_session(db=db, appointment_id=appointment_id)

@router.post("/webhook")
async def stripe_webhook_endpoint(request: Request, db: Session = Depends(get_db)):
    return await payments_service.stripe_webhook(db=db, request=request)