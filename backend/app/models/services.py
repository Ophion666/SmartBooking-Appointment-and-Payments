from app.db.session import Base
from sqlalchemy import Column, Integer, Float, String, Boolean


class Service(Base):

    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, index=True) 

    duration_minutes = Column(Integer)

    price = Column(Float)

    is_active = Column(Boolean, default=True)