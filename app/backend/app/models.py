from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="customer")
    provider = relationship("Provider", back_populates="user", uselist=False)

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    category = Column(String(80), nullable=False)
    description = Column(String(500), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    active = Column(Boolean, default=True, nullable=False)

class Provider(Base):
    __tablename__ = "providers"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    bio = Column(String(500), default="")
    user = relationship("User", back_populates="provider")
    availability = relationship("Availability", back_populates="provider")

class Availability(Base):
    __tablename__ = "availability"
    id = Column(Integer, primary_key=True)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    provider = relationship("Provider", back_populates="availability")
    __table_args__ = (UniqueConstraint("provider_id", "start_time", name="uq_provider_slot"),)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    appointment_time = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False, default="confirmed")
    customer = relationship("User")
    provider = relationship("Provider")
    service = relationship("Service")

