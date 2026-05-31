from sqlalchemy import Column, DateTime, Date, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class License(Base):
    __tablename__ = "licenses"
    id = Column(Integer, primary_key=True, index=True)
    license_holder_id = Column(Integer, ForeignKey("license_holders.id"), nullable=False, index=True)
    license_number = Column(String, nullable=False, unique=True, index=True)
    state = Column(String, nullable=False)
    expiration_date = Column(Date, nullable=False)
    ce_hours_required = Column(Integer, nullable=False)
    ce_hours_completed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    license_holder = relationship("LicenseHolder", back_populates="licenses")
    ce_courses = relationship("CECourse", back_populates="license")
    alert_logs = relationship("AlertLog", back_populates="license")
    