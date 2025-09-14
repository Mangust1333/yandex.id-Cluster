import uuid
from faker import Faker
from sqlalchemy import insert
from ..db import session
from ..truncate import truncate_table

from .V1_seed import UUID_USERS
from .V3_models import (
    RecoveryMethodType,
    RecoveryMethod,
    PhoneNumber,
    BackupEmail,
    SecurityQuestion,
    UserCredentials
)

faker = Faker("ru_RU")

UUID_RECOVERY_METHODS = []
UUID_PHONE_NUMBERS = []
UUID_EMAILS = []
UUID_SECURITY_QUESTIONS = []
UUID_CREDENTIALS = []

def truncate_v3_tables():
    truncate_table("recovery_methods")
    truncate_table("phone_numbers")
    truncate_table("backup_emails")
    truncate_table("security_questions")
    truncate_table("user_credentials")

def seed_recovery_methods():
    methods = []
    for user_id in UUID_USERS:
        method_id = uuid.uuid4()
        UUID_RECOVERY_METHODS.append(method_id)
        method_type = faker.random_element(["PHONE", "EMAIL", "SECURITY_QUESTION"])
        methods.append(RecoveryMethod(
            method_id=method_id,
            user_id=user_id,
            method_type=RecoveryMethodType[method_type],
            is_active=True
        ))
    session.bulk_save_objects(methods)
    session.commit()
    print(f"→ Засеяны recovery_methods: {len(methods)}")

def seed_phone_numbers():
    phone_numbers = []
    for user_id in UUID_USERS:
        phone_numbers.append(PhoneNumber(
            user_id=user_id,
            phone_number=faker.unique.phone_number(),
            is_verified=faker.boolean()
        ))
    session.bulk_save_objects(phone_numbers)
    session.commit()
    print(f"→ Засеяны phone_numbers: {len(phone_numbers)}")

def seed_backup_emails():
    emails = []
    for user_id in UUID_USERS:
        email_id = uuid.uuid4()
        UUID_EMAILS.append(email_id)
        emails.append(BackupEmail(
            email_id=email_id,
            user_id=user_id,
            email=faker.unique.email(),
            is_verified=faker.boolean()
        ))
    session.bulk_save_objects(emails)
    session.commit()
    print(f"→ Засеяны backup_emails: {len(emails)}")

def seed_security_questions():
    questions = []
    for user_id in UUID_USERS:
        questions.append(SecurityQuestion(
            user_id=user_id,
            question=faker.sentence(nb_words=6),
            answer=faker.word()
        ))
    session.bulk_save_objects(questions)
    session.commit()
    print(f"→ Засеяны security_questions: {len(questions)}")

def seed_user_credentials():
    credentials = []
    for user_id in UUID_USERS:
        credentials.append(UserCredentials(
            user_id=user_id,
            password_hash=faker.sha256(),
            password_salt=faker.md5(),
            password_last_changed=faker.date_time_this_decade()
        ))
    session.bulk_save_objects(credentials)
    session.commit()
    print(f"→ Засеяны user_credentials: {len(credentials)}")

def run_seed(SEED_COUNT):
    truncate_v3_tables()
    seed_recovery_methods()
    seed_phone_numbers()
    seed_backup_emails()
    seed_security_questions()
    seed_user_credentials()
    print("Сидирование для V3 завершено.")
