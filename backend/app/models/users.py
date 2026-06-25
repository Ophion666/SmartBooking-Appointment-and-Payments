from app.db.session import Base
from sqlalchemy import Column, Integer, String



class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    phone = Column(String, unique=True, index=True)