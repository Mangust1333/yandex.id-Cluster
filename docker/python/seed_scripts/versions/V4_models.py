import enum
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, TIMESTAMP, Enum, ForeignKey
from ..db import Base

class FamilyGroupRole(enum.Enum):
    ADMIN = "ADMIN"
    ADULT = "ADULT"
    CHILD = "CHILD"

class FamilyGroup(Base):
    __tablename__ = 'family_groups'

    group_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_name = Column(String(100))
    created_at = Column(TIMESTAMP)

class FamilyGroupMember(Base):
    __tablename__ = 'family_group_members'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    group_id = Column(UUID(as_uuid=True), ForeignKey('family_groups.group_id', ondelete='CASCADE'), primary_key=True)
    role = Column(Enum(FamilyGroupRole), nullable=False)
    added_at = Column(TIMESTAMP)
