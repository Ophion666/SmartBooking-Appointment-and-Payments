from app.db.session import Base
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship
from app.models.master_service import master_service_association

class Master(Base):

    __tablename__ = "masters"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    phone = Column(String, unique=True, index=True)

    specialization = Column(String)

    is_active = Column(Boolean, default=True)

    rating_avg = Column(Float, default=0)

    rating_count = Column(Integer, default=0)

    schedules = relationship("Schedule", back_populates="master")

    services = relationship("Service", secondary=master_service_association, back_populates="masters")