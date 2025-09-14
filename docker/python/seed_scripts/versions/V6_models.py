import enum
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Text, Enum, ForeignKey
from ..db import Base

class AddressType(enum.Enum):
    HOME = "HOME"
    WORK = "WORK"
    OTHER = "OTHER"

class Address(Base):
    __tablename__ = 'addresses'

    address_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name_of_address = Column(String(20))
    country = Column(String(100))
    region = Column(String(100))
    city = Column(String(100))
    street = Column(String(100))
    building = Column(String(10))

class UserAddress(Base):
    __tablename__ = 'user_addresses'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    address_id = Column(UUID(as_uuid=True), ForeignKey('addresses.address_id', ondelete='CASCADE'), primary_key=True)
    main_description = Column(Text)
    address_type = Column(Enum(AddressType), nullable=False)
    entrance = Column(String(10))
    floor = Column(String(10))
    apartment = Column(String(10))
    intercom = Column(String(10))
