import uuid
from faker import Faker
from sqlalchemy import insert
from ..db import session
from ..truncate import truncate_table
from .V1_seed import UUID_USERS
from .V4_models import FamilyGroup, FamilyGroupMember, FamilyGroupRole

faker = Faker("ru_RU")

UUID_FAMILY_GROUPS = []


def truncate_v4_tables():
    truncate_table("family_group_members")
    truncate_table("family_groups")

def seed_family_groups():
    groups = []
    for _ in range(10):
        group_id = uuid.uuid4()
        UUID_FAMILY_GROUPS.append(group_id)
        groups.append(FamilyGroup(
            group_id=group_id,
            group_name=faker.last_name() + " Family",
            created_at=faker.date_time_this_decade()
        ))
    session.bulk_save_objects(groups)
    session.commit()
    print(f"→ Засеяны family_groups: {len(groups)}")

def seed_family_group_members():
    members = []
    for user_id in UUID_USERS:
        group_id = faker.random_element(UUID_FAMILY_GROUPS)
        role = faker.random_element(["ADMIN", "ADULT", "CHILD"])
        members.append(FamilyGroupMember(
            user_id=user_id,
            group_id=group_id,
            role=FamilyGroupRole[role],
            added_at=faker.date_time_this_decade()
        ))
    session.bulk_save_objects(members)
    session.commit()
    print(f"→ Засеяны family_group_members: {len(members)}")

def run_seed(SEED_COUNT):
    truncate_v4_tables()
    seed_family_groups()
    seed_family_group_members()
    print("Сидирование для V4 завершено.")
