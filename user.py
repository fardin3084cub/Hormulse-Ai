"""
app/models/user.py — User model
"""
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
 
 
def gen_uuid() -> str:
    return str(uuid.uuid4())
 
 
class User(Base):
    __tablename__ = "users"
 
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(100), default="")
    goal: Mapped[str] = mapped_column(String(255), default="")
    struggle: Mapped[str] = mapped_column(String(255), default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    # Per-user API key (encrypted at rest)
    anthropic_api_key: Mapped[str] = mapped_column(Text, default="")
    preferred_provider: Mapped[str] = mapped_column(String(50), default="auto")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
 
    # relationships
    logs = relationship("WellnessLog", back_populates="user", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")
    plans = relationship("DailyPlan", back_populates="user", cascade="all, delete-orphan")
