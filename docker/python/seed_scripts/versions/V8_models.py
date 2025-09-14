import enum
import uuid
from sqlalchemy import Column, String, Date, Enum, Boolean, DECIMAL, CHAR, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from ..db import Base

class PaymentSystem(enum.Enum):
    VISA = 'VISA'
    MASTERCARD = 'MASTERCARD'
    MIR = 'MIR'
    AMEX = 'AMEX'
    JCB = 'JCB'
    UNIONPAY = 'UNIONPAY'

class TransactionStatus(enum.Enum):
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    CANCELED = 'CANCELED'

class TransactionType(enum.Enum):
    PAYMENT = 'PAYMENT'
    REFUND = 'REFUND'

class BankCard(Base):
    __tablename__ = 'bank_cards'

    bank_card_id = Column(CHAR(16), primary_key=True)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    cardholder_name = Column(String(100))
    expiration_date = Column(Date)
    payment_system = Column(Enum(PaymentSystem), nullable=False)
    bank_name = Column(String(100))
    is_default = Column(Boolean, nullable=False, default=False)

class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    bank_card_id = Column(CHAR(16), ForeignKey('bank_cards.bank_card_id', ondelete='CASCADE'), nullable=False)
    service_id = Column(PG_UUID(as_uuid=True), ForeignKey('services.service_id', ondelete='SET NULL'), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(CHAR(3), nullable=False)
    status = Column(Enum(TransactionStatus), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    description = Column(String(255))
    created_at = Column(TIMESTAMP, nullable=False)
    receipt = Column(String(100), unique=True)
