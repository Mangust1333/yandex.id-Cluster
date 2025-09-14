import enum
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column, String, Boolean, Text, ForeignKey,
    Enum, TIMESTAMP, func
)
from ..db import Base

class DeviceType(enum.Enum):
    SMARTPHONE = "SMARTPHONE"
    TABLET = "TABLET"
    PC = "PC"
    LAPTOP = "LAPTOP"
    OTHER = "OTHER"

class User(Base):
    __tablename__ = 'users'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = Column(String(32), unique=True, nullable=False)
    avatar = Column(Text, unique=True)
    is_premium_user = Column(Boolean, default=False)

    roles = relationship("UserRole", back_populates="user", cascade="all, delete")
    devices = relationship("Device", back_populates="user", cascade="all, delete")
    activity = relationship("ActivityHistory", back_populates="user", cascade="all, delete")

class Role(Base):
    __tablename__ = 'roles'

    role_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role = Column(String(20), nullable=False)

    user_roles = relationship("UserRole", back_populates="role", cascade="all, delete")

class UserRole(Base):
    __tablename__ = 'user_roles'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.role_id', ondelete='CASCADE'), nullable=False)

    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="user_roles")

class Action(Base):
    __tablename__ = 'actions'

    action_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action_name = Column(String(100), unique=True, nullable=False)
    action_description = Column(Text)

    activities = relationship("ActivityHistory", back_populates="action", cascade="all, delete")

class Device(Base):
    __tablename__ = 'devices'

    device_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    device_type = Column(Enum(DeviceType), nullable=False)
    device_name = Column(String(100), nullable=False)
    os = Column(String(50), nullable=False)
    os_version = Column(String(50))
    last_login = Column(TIMESTAMP)
    last_ip = Column(String(45))
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="devices")
    activity = relationship("ActivityHistory", back_populates="device", cascade="all, delete")

class ActivityHistory(Base):
    __tablename__ = 'activity_history'

    activity_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    device_id = Column(UUID(as_uuid=True), ForeignKey('devices.device_id', ondelete='CASCADE'), nullable=False)
    action_id = Column(UUID(as_uuid=True), ForeignKey('actions.action_id', ondelete='CASCADE'), nullable=False)
    details = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="activity")
    device = relationship("Device", back_populates="activity")
    action = relationship("Action", back_populates="activities")