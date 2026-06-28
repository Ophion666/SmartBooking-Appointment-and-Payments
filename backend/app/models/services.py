from app.db.session import Base
from sqlalchemy import Column, Integer, Float, String, Boolean
from sqlalchemy.orm import relationship
from app.models.master_service import master_service_association

class Service(Base):

    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, index=True) 

    duration_minutes = Column(Integer)

    price = Column(Float)

    is_active = Column(Boolean, default=True)

    masters = relationship("Master", secondary=master_service_association, back_populates="services")