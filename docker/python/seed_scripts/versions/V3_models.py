import enum
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column, String, Boolean, ForeignKey,
    Enum, TIMESTAMP
)
from ..db import Base

class RecoveryMethodType(enum.Enum):
    PHONE = "PHONE"
    EMAIL = "EMAIL"
    SECURITY_QUESTION = "SECURITY_QUESTION"

class RecoveryMethod(Base):
    __tablename__ = 'recovery_methods'

    method_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    method_type = Column(Enum(RecoveryMethodType), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

class PhoneNumber(Base):
    __tablename__ = 'phone_numbers'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    phone_number = Column(String(22), nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

class BackupEmail(Base):
    __tablename__ = 'backup_emails'

    email_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    email = Column(String(100), nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

class SecurityQuestion(Base):
    __tablename__ = 'security_questions'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    question = Column(String(255), nullable=False)
    answer = Column(String(255), nullable=False)

class UserCredentials(Base):
    __tablename__ = 'user_credentials'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    password_hash = Column(String(255), nullable=False)
    password_salt = Column(String(255), nullable=False)
    password_last_changed = Column(TIMESTAMP)
