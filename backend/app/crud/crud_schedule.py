from sqlalchemy.orm import Session
from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate
from app.schemas.schedule import DayOfWeek

def create_schedule(db: Session, schedule: ScheduleCreate):
    db_schedule = Schedule(
        master_id = schedule.master_id,
        day_of_week = schedule.day_of_week, start_time = schedule.start_time,
        end_time = schedule.end_time
        )
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def get_schedule_by_id(db: Session, id: int):
    return db.query(Schedule).filter(Schedule.id == id).first()

def get_all_schedule(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Schedule).offset(skip).limit(limit).all()


def get_schedule_by_master_and_day(db: Session, master_id: int, day_of_week: DayOfWeek):
    return db.query(Schedule).filter(
        Schedule.master_id == master_id,
        Schedule.day_of_week == day_of_week
    ).first()