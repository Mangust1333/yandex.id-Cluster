import enum
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey, Enum, Text
from ..db import Base

class SupportSessionStatus(enum.Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    PENDING = "PENDING"

class SupportMessagesSenderType(enum.Enum):
    USER = "USER"
    AGENT = "AGENT"

class SupportMessagesReactionType(enum.Enum):
    NONE = "NONE"
    LIKE = "LIKE"
    DISLIKE = "DISLIKE"
    LAUGH = "LAUGH"
    LOVE = "LOVE"
    SAD = "SAD"
    ANGRY = "ANGRY"

class SupportAgent(Base):
    __tablename__ = 'support_agents'

    agent_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_name = Column(String(100))
    email = Column(String(100), unique=True)
    created_at = Column(TIMESTAMP)
    is_active = Column(Boolean, nullable=False, default=True)

class SupportSession(Base):
    __tablename__ = 'support_sessions'

    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    agent_id = Column(UUID(as_uuid=True), ForeignKey('support_agents.agent_id', ondelete='SET NULL'))
    session_status = Column(Enum(SupportSessionStatus), nullable=False)
    started_at = Column(TIMESTAMP)
    closed_at = Column(TIMESTAMP)

class SupportMessage(Base):
    __tablename__ = 'support_messages'

    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey('support_sessions.session_id', ondelete='CASCADE'), nullable=False)
    sender = Column(Enum(SupportMessagesSenderType), nullable=False)
    reaction_type = Column(Enum(SupportMessagesReactionType), nullable=False, default=SupportMessagesReactionType.NONE)
    message_text = Column(Text)
    sent_at = Column(TIMESTAMP)

class SupportMessageAttachment(Base):
    __tablename__ = 'support_message_attachments'

    attachment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = Column(UUID(as_uuid=True), ForeignKey('support_messages.message_id', ondelete='CASCADE'), nullable=False)
    file_url = Column(String(255))
    file_type = Column(String(50))
    uploaded_at = Column(TIMESTAMP)
