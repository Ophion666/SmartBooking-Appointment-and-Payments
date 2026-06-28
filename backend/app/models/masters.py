from app.db.session import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.models.master_service import master_service_association

class Master(Base):

    __tablename__ = "masters"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    phone = Column(String, unique=True, index=True)

    specialization = Column(String)

    is_active = Column(Boolean, default=True)

    schedules = relationship("Schedule", back_populates="master")

    services = relationship("Service", secondary=master_service_association, back_populates="masters")