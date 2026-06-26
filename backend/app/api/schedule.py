from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import schedule
from app.crud import crud_schedule
from app.crud.crud_master import get_master_by_id
from app.models.users import User
from app.services.current_admin import get_current_admin



router = APIRouter(prefix="/schedule", tags=["Schedules"])

@router.post("/create_schedule", response_model=schedule.ScheduleResponse)
def post_create_shedule(schedule: schedule.ScheduleCreate, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
  
    check_master = get_master_by_id(db, master_id = schedule.master_id )
    if not check_master:
        raise HTTPException(status_code=404, detail="Master not found")
    
    if schedule.start_time >= schedule.end_time:
        raise HTTPException(status_code=400, detail="Incorrect Time")
    
    existing_schedule = crud_schedule.get_schedule_by_master_and_day(
        db=db,
        master_id=schedule.master_id,
        day_of_week=schedule.day_of_week
    )

    if existing_schedule:
        raise HTTPException(status_code=400, detail="Master already has a schedule for this day")
    
    return crud_schedule.create_schedule(db=db, schedule=schedule)
    

@router.get("/schedules", response_model=list[schedule.ScheduleResponse])
def get_schedule(db: Session = Depends(get_db)):
    return crud_schedule.get_all_schedule(db=db)