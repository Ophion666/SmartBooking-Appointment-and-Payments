from app.db.session import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, SmallInteger, CheckConstraint
from sqlalchemy.sql import func

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), unique=True, nullable=False)
    master_id = Column(Integer, ForeignKey("masters.id"), nullable=False)
    score = Column(SmallInteger, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        CheckConstraint("score >= 1 AND score <= 5", name="check_score_range"),
    )