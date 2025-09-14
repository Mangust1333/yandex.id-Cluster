import uuid
from faker import Faker
from ..db import session
from ..truncate import truncate_table
from .V1_seed import UUID_USERS
from .V6_seed import UUID_ADDRESSES
from .V7_models import (
    NotificationType, NotificationNameType,
    Service, ServiceAddressNote,
    ServiceNotificationType, UserServiceNotificationDisabled
)
from .V6_models import Address, UserAddress, AddressType


faker = Faker("ru_RU")

UUID_NOTIFICATION_TYPES = []
UUID_SERVICES = []
UUID_SERVICE_NOTIFICATION_TYPES = []

def truncate_v7_tables():
    truncate_table("user_service_notification_disabled")
    truncate_table("service_notification_types")
    truncate_table("service_address_notes")
    truncate_table("services")
    truncate_table("notification_types")

def seed_notification_types():
    types = []
    for name in NotificationNameType:
        nt_id = uuid.uuid4()
        UUID_NOTIFICATION_TYPES.append(nt_id)
        types.append(NotificationType(
            notification_type_id=nt_id,
            type_name=name,
            description=faker.sentence()
        ))
    session.bulk_save_objects(types)
    session.commit()
    print(f"→ Засеяны notification_types: {len(types)}")

def seed_services():
    services = []
    for _ in range(5):
        service_id = uuid.uuid4()
        UUID_SERVICES.append(service_id)
        services.append(Service(
            service_id=service_id,
            service_name=faker.word()
        ))
    session.bulk_save_objects(services)
    session.commit()
    print(f"→ Засеяны services: {len(services)}")

def seed_service_address_notes():
    notes = []
    for user_id, address_id in zip(UUID_USERS, UUID_ADDRESSES):
        service_id = faker.random_element(UUID_SERVICES)
        notes.append(ServiceAddressNote(
            user_id=user_id,
            addresses_id=address_id,
            service_id=service_id,
            description=faker.sentence()
        ))
    session.add_all(notes)
    session.commit()
    print(f"→ Засеяны service_address_notes: {len(notes)}")

def seed_service_notification_types():
    records = []
    for service_id in UUID_SERVICES:
        for nt_id in faker.random_elements(UUID_NOTIFICATION_TYPES, length=3, unique=True):
            snt_id = uuid.uuid4()
            UUID_SERVICE_NOTIFICATION_TYPES.append(snt_id)
            records.append(ServiceNotificationType(
                service_notification_type_id=snt_id,
                service_id=service_id,
                notification_type_id=nt_id
            ))
    session.bulk_save_objects(records)
    session.commit()
    print(f"→ Засеяны service_notification_types: {len(records)}")

def seed_user_service_notification_disabled():
    disabled = []
    for user_id in UUID_USERS:
        snt_id = faker.random_element(UUID_SERVICE_NOTIFICATION_TYPES)
        disabled.append(UserServiceNotificationDisabled(
            user_id=user_id,
            service_notification_type_id=snt_id
        ))
    session.bulk_save_objects(disabled)
    session.commit()
    print(f"→ Засеяны user_service_notification_disabled: {len(disabled)}")

def run_seed(SEED_COUNT):
    truncate_v7_tables()
    seed_notification_types()
    seed_services()
    seed_service_address_notes()
    seed_service_notification_types()
    seed_user_service_notification_disabled()
    print("Сидирование для V7 завершено.")
