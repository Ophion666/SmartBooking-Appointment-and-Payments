from app.db.session import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Master(Base):

    __tablename__ = "masters"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    phone = Column(String, unique=True, index=True)

    specialization = Column(String)

    schedules = relationship("Schedule", back_populates="master")