from app.db.session import Base
from sqlalchemy import Column, Integer, ForeignKey, Time
from app.schemas.schedule import DayOfWeek
from sqlalchemy import Enum as sqlalchemy_Enum
from sqlalchemy.orm import relationship

class Schedule(Base):

    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)

    master_id = Column(Integer, ForeignKey("masters.id"))

    day_of_week = Column(sqlalchemy_Enum(DayOfWeek))

    start_time = Column(Time)

    end_time = Column(Time)

    master = relationship("Master",  back_populates="schedules")