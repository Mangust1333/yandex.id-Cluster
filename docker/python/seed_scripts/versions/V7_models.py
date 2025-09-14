import enum
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKeyConstraint, String, Text, Enum, ForeignKey
from .V6_models import UserAddress
from ..db import Base

class NotificationNameType(enum.Enum):
    CALL = "CALL"
    PUSH = "PUSH"
    SMS = "SMS"
    EMAIL = "EMAIL"
    OTHER = "OTHER"

class NotificationType(Base):
    __tablename__ = 'notification_types'

    notification_type_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type_name = Column(Enum(NotificationNameType), nullable=False)
    description = Column(String(255))

class Service(Base):
    __tablename__ = 'services'

    service_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_name = Column(String(100), nullable=False)

class ServiceAddressNote(Base):
    __tablename__ = 'service_address_notes'

    user_id = Column(UUID(as_uuid=True), primary_key=True)
    addresses_id = Column(UUID(as_uuid=True), primary_key=True)
    service_id = Column(UUID(as_uuid=True), ForeignKey('services.service_id', ondelete='CASCADE'), primary_key=True)
    description = Column(Text)

    __table_args__ = (
        ForeignKeyConstraint(
            ['user_id', 'addresses_id'],
            [UserAddress.user_id, UserAddress.address_id],
            ondelete='CASCADE'
        ),
    )


class ServiceNotificationType(Base):
    __tablename__ = 'service_notification_types'

    service_notification_type_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_id = Column(UUID(as_uuid=True), ForeignKey('services.service_id', ondelete='CASCADE'), nullable=False)
    notification_type_id = Column(UUID(as_uuid=True), ForeignKey('notification_types.notification_type_id', ondelete='CASCADE'), nullable=False)

class UserServiceNotificationDisabled(Base):
    __tablename__ = 'user_service_notification_disabled'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    service_notification_type_id = Column(UUID(as_uuid=True), ForeignKey('service_notification_types.service_notification_type_id', ondelete='CASCADE'), primary_key=True)
