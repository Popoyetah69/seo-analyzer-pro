from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, UniqueConstraint
from sqlalchemy.sql import func
from datetime import datetime
from database import Base

class User(Base):
    """Customer user with subscription info"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)
    stripe_customer_id = Column(String(255), unique=True, nullable=True, index=True)
    plan = Column(String(50), default="free")  # free, starter, professional, enterprise
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Subscription(Base):
    """Stripe subscription tracking"""
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    stripe_subscription_id = Column(String(255), unique=True, index=True, nullable=False)
    stripe_customer_id = Column(String(255), index=True, nullable=False)
    plan = Column(String(50), nullable=False)  # starter, professional, enterprise
    status = Column(String(50), nullable=False)  # active, past_due, canceled, etc.
    current_period_start = Column(DateTime, nullable=True)
    current_period_end = Column(DateTime, nullable=True)
    cancel_at = Column(DateTime, nullable=True)
    canceled_at = Column(DateTime, nullable=True)
    payment_failed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WebhookEvent(Base):
    """Webhook event log (for idempotence and audit)"""
    __tablename__ = "webhook_events"
    
    id = Column(Integer, primary_key=True, index=True)
    stripe_event_id = Column(String(255), unique=True, index=True, nullable=False)
    event_type = Column(String(100), index=True, nullable=False)
    customer_id = Column(String(255), index=True, nullable=True)
    subscription_id = Column(String(255), index=True, nullable=True)
    status = Column(String(50), default="received")  # received, processed, failed
    payload = Column(Text, nullable=True)  # Store full JSON payload
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        UniqueConstraint('stripe_event_id', name='_stripe_event_id_uc'),
    )
