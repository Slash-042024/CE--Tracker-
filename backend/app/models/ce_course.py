from sqlalchemy import Column, DateTime, Date, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class CECourse(Base):
    __tablename__ = "ce_courses"
    id = Column(Integer, primary_key=True, index=True)
    license_id = Column(Integer, ForeignKey("licenses.id"), nullable=False, index=True)
    course_name = Column(String, nullable=False)
    course_provider = Column(String, nullable=False)
    date_completed = Column(Date, nullable=False)
    hours_earned = Column(Integer, nullable=False)
    certificate_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    license = relationship("License", back_populates="ce_courses")