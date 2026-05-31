from sqlalchemy import Column, DateTime, Date, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class AlertLog(Base):
    __tablename__ = "alert_logs"
    id = Column(Integer, primary_key=True, index=True)
    license_id = Column(Integer, ForeignKey("licenses.id"), nullable=False, index=True)
    alert_method = Column(String, nullable=False)
    sent_to = Column(String, nullable=False)
    days_remaining = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    license = relationship("License", back_populates="alert_logs")