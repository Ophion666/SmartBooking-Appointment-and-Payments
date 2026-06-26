from sqlalchemy import Column, Integer, ForeignKey, Table
from app.db.session import Base

master_service_association = Table(
    "master_service",
    Base.metadata,
    Column("master_id", Integer, ForeignKey("master.id"), primary_key=True),
    Column("service_id", Integer, ForeignKey("services.id"), primary_key=True)
)