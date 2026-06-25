from app.db.session import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy import Enum as sqlalchemy_Enum
from app.schemas.appointments import AppointmentStatus
from sqlalchemy.orm import relationship

class Appointment(Base):

    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    master_id = Column(Integer, ForeignKey("masters.id"))

    service_id = Column(Integer, ForeignKey("services.id"))

    start_datetime = Column(DateTime)

    status = Column(sqlalchemy_Enum(AppointmentStatus))

    user = relationship("User", backref="appointments")

    master = relationship("Master", backref="appointments")
    
    service = relationship("Service")