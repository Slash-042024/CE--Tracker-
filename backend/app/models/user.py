from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    phone = Column(String)
    password_hash = Column(String)
    account_type = Column(String, default="customer")
    stripe_customer_id = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    license_holders = relationship("LicenseHolder", back_populates="user")
    subscriptions= relationship("Subscription", back_populates="user")

    