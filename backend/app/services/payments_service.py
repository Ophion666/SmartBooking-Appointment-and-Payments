import os
import stripe
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from app.crud import crud_appointment
from app.schemas.appointments import AppointmentStatus
from app.api.worker import send_telegram_task
from app.services.appointment_service import active_timers

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

def create_checkout_session(appointment_id: int, db: Session):

    appointment = crud_appointment.get_appointment_by_id(db, appointment_id=appointment_id)

    if not appointment:
         raise HTTPException(status_code=404, detail="Appointment not found")
    
    if appointment.status != AppointmentStatus.pending_payment:
         raise HTTPException(status_code=400, detail="This appointment already payed or cancelled")
    
    service = appointment.service

    amount_in_cents = int(service.price * 100)

    try:
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd', 
                        'product_data': {
                            'name': f"Appointment payment: {service.name}",
                            'description': f"Master: {appointment.master.name} | Time: {appointment.start_datetime.strftime('%d.%m.%Y %H:%M')}"
                        },
                        'unit_amount': amount_in_cents,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            
            success_url='http://localhost:8000/docs', 
            cancel_url='http://localhost:8000/docs',
            
            
            
            metadata={
                "appointment_id": appointment.id
            }
        )
        
        
        return {"checkout_url": checkout_session.url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

async def stripe_webhook(request: Request, db: Session):

    payload = await request.body()

    sig_header = request.headers.get("Stripe-Signature")

    try:

        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid payload")
    
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        if session.metadata:
            appointment_id_str = session.metadata.appointment_id
            appointment_id = int(appointment_id_str)
            appointment = crud_appointment.get_appointment_by_id(db, appointment_id=appointment_id)

            if appointment:
                payment_intent_id = getattr(session, "payment_intent", None)


                if appointment.status == AppointmentStatus.pending_payment:
                    appointment.status = AppointmentStatus.confirmed
                    appointment.stripe_payment_id = payment_intent_id
                    db.commit()

                    if appointment_id in active_timers:
                        active_timers[appointment_id].set()

                    cancel_url = f"http://localhost:8000/booking/cancel/{appointment.cancel_token}"

                    text = (
                        f"<b>PAYMENT SUCCESS</b>\n"
                        f"appointment #{appointment_id} confirmed"
                        f"<b>Url for cancel</b>\n{cancel_url}"
                    )
                    send_telegram_task.delay(text)

                elif appointment.status == AppointmentStatus.cancelled:
                    
                    payment_intent_id = session.payment_intent

                    if payment_intent_id:

                        stripe.Refund.create(payment_intent=payment_intent_id)

    return {"status": "success"}