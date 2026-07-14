from fastapi import FastAPI
from app.api import users, masters, services, schedule, booking, appointments, admin, payments, rating


app = FastAPI(title="SmartBooking API")
app.include_router(users.router)
app.include_router(masters.router)
app.include_router(services.router)
app.include_router(schedule.router)
app.include_router(booking.router)
app.include_router(appointments.router)
app.include_router(admin.router)
app.include_router(payments.router)
app.include_router(rating.router)