import enum
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    String,
    Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    EDITOR = "EDITOR"
    # VIEWER = "VIEWER"
    USER = "user"  # Default role for new users, can be changed later


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    username: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True, nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    
    role: Mapped[str] = mapped_column(String(50), default=UserRole.USER.value, nullable=False)
    status: Mapped[Optional[str]] = mapped_column(String(50), default="pending", nullable=True)
    auth_provider: Mapped[Optional[str]] = mapped_column(String(50), default="local", nullable=True)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    must_change_password: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    hris_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    facility_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    lab_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    mobile: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    division_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    district_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    upazila_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    union_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    projects: Mapped[List["Project"]] = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    refresh_sessions: Mapped[List["RefreshToken"]] = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    owner_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Many-to-1 Relationship: Many Projects belong to One User
    owner: Mapped["User"] = relationship("User", back_populates="projects")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationship back to the user
    user: Mapped["User"] = relationship("User", back_populates="refresh_sessions")