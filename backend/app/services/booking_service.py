from datetime import date, datetime, timedelta
from app.schemas.schedule import DayOfWeek
from fastapi import HTTPException
from app.crud import crud_schedule, crud_appointment, crud_service
from datetime import date, datetime, timedelta
import math
from app.schemas.schedule import DayOfWeek
from sqlalchemy.orm import Session


def get_available_slots(master_id: int,service_id: int , target_date: date, db: Session):

    service = crud_service.get_service_by_id(db, service_id=service_id)

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    slots_needed = math.ceil(service.duration_minutes / 30)

    days_map = {
        0: DayOfWeek.Monday,
        1: DayOfWeek.Tuesday,
        2: DayOfWeek.Wednesday,
        3: DayOfWeek.Thursday,
        4: DayOfWeek.Friday,
        5: DayOfWeek.Saturday,
        6: DayOfWeek.Sunday
    }
    day_enum = days_map[target_date.weekday()]
    master_day = crud_schedule.get_schedule_by_master_and_day(db, master_id = master_id, day_of_week= day_enum )

    if not master_day:
        return {"message": "Weekend"}

    appointments = crud_appointment.get_appointments_by_master_and_date(db, master_id, target_date)
    booked_slots = set()
    
    for appt in appointments:
        duration = appt.service.duration_minutes

        count = math.ceil(duration / 30)

        for i in range(count):

            blocked_time = appt.start_datetime + timedelta(minutes= 30 * i)
            booked_slots.add(blocked_time.strftime("%H:%M"))

    slots = []
    slot_duration = timedelta(minutes=30)
    current_time = datetime.combine(target_date, master_day.start_time)
    end_time = datetime.combine(target_date, master_day.end_time)

    service_total_duration = timedelta(minutes=30 * slots_needed)

    while current_time + slot_duration <= end_time:

        if current_time < datetime.now(): 
            current_time += slot_duration
            continue

        is_free = True

        for i in range(slots_needed):
            check_time_str = (current_time + timedelta(minutes=30 * i)).strftime("%H:%M")

            if check_time_str in booked_slots:
                is_free = False
                break
                
        if is_free:
            slots.append(current_time.strftime("%H:%M"))
        
        current_time += slot_duration


    return {"date": target_date, "available_slots": slots}
