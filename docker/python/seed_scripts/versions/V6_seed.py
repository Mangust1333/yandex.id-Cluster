import uuid
from faker import Faker
from ..db import session
from ..truncate import truncate_table
from .V1_seed import UUID_USERS
from .V6_models import Address, UserAddress, AddressType

faker = Faker("ru_RU")

UUID_ADDRESSES = []

def truncate_v6_tables():
    truncate_table("user_addresses")
    truncate_table("addresses")

def seed_addresses():
    addresses = []
    for _ in range(len(UUID_USERS)):
        address_id = uuid.uuid4()
        UUID_ADDRESSES.append(address_id)
        addresses.append(Address(
            address_id=address_id,
            name_of_address=faker.word(),
            country="Россия",
            region=faker.region(),
            city=faker.city(),
            street=faker.street_name(),
            building=faker.building_number()
        ))
    session.bulk_save_objects(addresses)
    session.commit()
    print(f"→ Засеяны addresses: {len(addresses)}")

def seed_user_addresses():
    user_addresses = []
    for idx, user_id in enumerate(UUID_USERS):
        address_id = UUID_ADDRESSES[idx]
        addr_type = faker.random_element(["HOME", "WORK", "OTHER"])
        user_addresses.append(UserAddress(
            user_id=user_id,
            address_id=address_id,
            main_description=faker.sentence(nb_words=6),
            address_type=AddressType[addr_type],
            entrance=str(faker.random_int(min=1, max=5)),
            floor=str(faker.random_int(min=1, max=20)),
            apartment=str(faker.random_int(min=1, max=300)),
            intercom=str(faker.random_int(min=10, max=99))
        ))
    session.bulk_save_objects(user_addresses)
    session.commit()
    print(f"→ Засеяны user_addresses: {len(user_addresses)}")

def run_seed(SEED_COUNT):
    truncate_v6_tables()
    seed_addresses()
    seed_user_addresses()
    print("Сидирование для V6 завершено.")
