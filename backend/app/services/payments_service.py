import os
import stripe
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_appointment
from app.schemas.appointments import AppointmentStatus

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

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