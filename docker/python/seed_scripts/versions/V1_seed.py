from faker import Faker
import uuid
from ..db import session
from .V1_models import User, Role, UserRole, Device, Action, ActivityHistory, DeviceType
from ..truncate import truncate_table

faker = Faker("ru_RU")

UUID_USERS = []
UUID_DEVICES = []
UUID_ACTIONS = []
UUID_ROLES = []

USER_NORM=10
ACTIONS_NORM=10

def generate_user_uuids(count):
    global UUID_USERS, USER_NORM
    UUID_USERS = [uuid.uuid4() for _ in range(count * USER_NORM)]

def seed_users():
    users = []
    for user_uuid in UUID_USERS:
        user = User(
            user_id=user_uuid,
            login=faker.unique.user_name(),
            avatar=faker.unique.image_url(),
            is_premium_user=faker.boolean()
        )
        users.append(user)
    session.bulk_save_objects(users)
    session.commit()
    print(f"→ Засеяно {len(users)} пользователей")

def seed_roles():
    roles = ['user', 'admin', 'moderator', 'support']
    objects = []
    for role in roles:
        role_obj = Role(role_id=uuid.uuid4(), role=role)
        UUID_ROLES.append(role_obj.role_id)
        objects.append(role_obj)
    session.bulk_save_objects(objects)
    session.commit()
    print("→ Засеяны роли")

def seed_user_roles():
    objects = []
    for user_id in UUID_USERS:
        role_id = faker.random_element(UUID_ROLES)
        ur = UserRole(user_id=user_id, role_id=role_id)
        objects.append(ur)
    session.bulk_save_objects(objects)
    session.commit()
    print("→ Засеяны user_roles")

def seed_devices():
    devices = []
    for user_id in UUID_USERS:
        device_id = uuid.uuid4()
        UUID_DEVICES.append(device_id)
        d = Device(
            device_id=device_id,
            user_id=user_id,
            device_type=faker.random_element(DeviceType),
            device_name=faker.hostname(),
            os=faker.unix_device(),
            os_version=faker.numerify(text="##.##"),
            last_login=faker.date_time_this_year(),
            last_ip=faker.ipv4()
        )
        devices.append(d)
    session.bulk_save_objects(devices)
    session.commit()
    print("→ Засеяны устройства")

def seed_actions():
    actions = []
    for _ in range(5):
        action_id = uuid.uuid4()
        UUID_ACTIONS.append(action_id)
        a = Action(
            action_id=action_id,
            action_name=faker.unique.bs(),
            action_description=faker.sentence()
        )
        actions.append(a)
    session.bulk_save_objects(actions)
    session.commit()
    print("→ Засеяны действия")

def seed_activity_history():
    activities = []
    for _ in range(len(UUID_USERS) * ACTIONS_NORM):
        ah = ActivityHistory(
            activity_id=uuid.uuid4(),
            user_id=faker.random_element(UUID_USERS),
            device_id=faker.random_element(UUID_DEVICES),
            action_id=faker.random_element(UUID_ACTIONS),
            details=faker.sentence()
        )
        activities.append(ah)
    session.bulk_save_objects(activities)
    session.commit()
    print("→ Засеяна история активности")

def run_seed(SEED_COUNT):
    truncate_table(User.__tablename__)
    truncate_table(Role.__tablename__)
    truncate_table(UserRole.__tablename__)
    truncate_table(Device.__tablename__)
    truncate_table(Action.__tablename__)
    truncate_table(ActivityHistory.__tablename__)
    generate_user_uuids(SEED_COUNT)
    seed_users()
    seed_roles()
    seed_user_roles()
    seed_devices()
    seed_actions()
    seed_activity_history()
    print("Сидирование для V1 завершено.")
    print(f"✓ Создано: {len(UUID_USERS)} пользователей, {len(UUID_ACTIONS)} действий, {len(UUID_DEVICES)} устройств.")


