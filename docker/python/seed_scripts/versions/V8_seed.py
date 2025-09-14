import uuid
import random
from datetime import datetime, timedelta
from faker import Faker
from ..db import session
from ..truncate import truncate_table
from .V1_seed import UUID_USERS
from .V7_seed import UUID_SERVICES
from .V8_models import (
    BankCard, Transaction,
    PaymentSystem, TransactionStatus, TransactionType
)

faker = Faker("ru_RU")

UUID_BANK_CARDS = []
UUID_TRANSACTIONS = []

def truncate_v8_tables():
    truncate_table("transactions")
    truncate_table("bank_cards")

def seed_bank_cards():
    for user_id in UUID_USERS:
        for _ in range(2):  # по 2 карты на пользователя
            card_id = ''.join(faker.random_choices(elements='0123456789', length=16))
            UUID_BANK_CARDS.append(card_id)
            card = BankCard(
                bank_card_id=card_id,
                user_id=user_id,
                cardholder_name=faker.name(),
                expiration_date=faker.date_between(start_date='today', end_date='+3y'),
                payment_system=random.choice(list(PaymentSystem)),
                bank_name=faker.company(),
                is_default=faker.boolean(chance_of_getting_true=30)
            )
            session.add(card)
    session.commit()
    print(f"→ Засеяны bank_cards: {len(UUID_BANK_CARDS)}")

def seed_transactions():
    for _ in range(len(UUID_USERS) * 3):  # по 3 транзакции на пользователя
        transaction = Transaction(
            transaction_id=uuid.uuid4(),
            user_id=random.choice(UUID_USERS),
            bank_card_id=random.choice(UUID_BANK_CARDS),
            service_id=random.choice(UUID_SERVICES),
            amount=round(random.uniform(10, 1000), 2),
            currency="RUB",
            status=random.choice(list(TransactionStatus)),
            transaction_type=random.choice(list(TransactionType)),
            description=faker.sentence(),
            created_at=faker.date_time_between(start_date='-1y', end_date='now'),
            receipt=str(uuid.uuid4())
        )
        UUID_TRANSACTIONS.append(transaction.transaction_id)
        session.add(transaction)
    session.commit()
    print(f"→ Засеяны transactions: {len(UUID_TRANSACTIONS)}")

def run_seed(SEED_COUNT):
    truncate_v8_tables()
    seed_bank_cards()
    seed_transactions()
    print("Сидирование для V8 завершено.")
