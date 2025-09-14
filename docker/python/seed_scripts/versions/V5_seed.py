import uuid
from faker import Faker
from ..db import session
from ..truncate import truncate_table
from .V1_seed import UUID_USERS
from .V5_models import (
    SupportAgent,
    SupportSession,
    SupportMessage,
    SupportMessageAttachment,
    SupportSessionStatus,
    SupportMessagesSenderType,
    SupportMessagesReactionType
)

faker = Faker("ru_RU")

UUID_AGENTS = []
UUID_SESSIONS = []
UUID_MESSAGES = []

def truncate_v5_tables():
    truncate_table("support_message_attachments")
    truncate_table("support_messages")
    truncate_table("support_sessions")
    truncate_table("support_agents")

def seed_support_agents():
    agents = []
    for _ in range(100):
        agent_id = uuid.uuid4()
        UUID_AGENTS.append(agent_id)
        agents.append(SupportAgent(
            agent_id=agent_id,
            agent_name=faker.name(),
            email=faker.unique.email(),
            created_at=faker.date_time_this_decade(),
            is_active=True
        ))
    session.bulk_save_objects(agents)
    session.commit()
    print(f"→ Засеяны support_agents: {len(agents)}")

def seed_support_sessions():
    sessions = []
    for user_id in UUID_USERS:
        session_id = uuid.uuid4()
        UUID_SESSIONS.append(session_id)
        sessions.append(SupportSession(
            session_id=session_id,
            user_id=user_id,
            agent_id=faker.random_element(UUID_AGENTS),
            session_status=faker.random_element(list(SupportSessionStatus)),
            started_at=faker.date_time_this_decade(),
            closed_at=faker.date_time_this_decade()
        ))
    session.bulk_save_objects(sessions)
    session.commit()
    print(f"→ Засеяны support_sessions: {len(sessions)}")

def seed_support_messages():
    messages = []
    for session_id in UUID_SESSIONS:
        for _ in range(faker.random_int(min=1, max=20)):
            message_id = uuid.uuid4()
            UUID_MESSAGES.append(message_id)
            messages.append(SupportMessage(
                message_id=message_id,
                session_id=session_id,
                sender=faker.random_element(list(SupportMessagesSenderType)),
                reaction_type=faker.random_element(list(SupportMessagesReactionType)),
                message_text=faker.text(max_nb_chars=200),
                sent_at=faker.date_time_this_decade()
            ))
    session.bulk_save_objects(messages)
    session.commit()
    print(f"→ Засеяны support_messages: {len(messages)}")

def seed_support_attachments():
    attachments = []
    for message_id in UUID_MESSAGES:
        if faker.boolean(chance_of_getting_true=40):  # 40% сообщений с вложениями
            attachments.append(SupportMessageAttachment(
                attachment_id=uuid.uuid4(),
                message_id=message_id,
                file_url=faker.image_url(),
                file_type=faker.file_extension(category="image"),
                uploaded_at=faker.date_time_this_decade()
            ))
    session.bulk_save_objects(attachments)
    session.commit()
    print(f"→ Засеяны support_message_attachments: {len(attachments)}")

def run_seed(SEED_COUNT):
    truncate_v5_tables()
    seed_support_agents()
    seed_support_sessions()
    seed_support_messages()
    seed_support_attachments()
    print("Сидирование для V5 завершено.")
