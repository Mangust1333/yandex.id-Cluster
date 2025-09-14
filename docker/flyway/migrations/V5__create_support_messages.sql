CREATE TYPE support_session_status AS ENUM ('OPEN', 'CLOSED', 'PENDING');
CREATE TYPE support_messages_sender_type AS ENUM ('USER', 'AGENT');
CREATE TYPE support_messages_reaction_type AS ENUM ('NONE', 'LIKE', 'DISLIKE', 'LAUGH', 'LOVE', 'SAD', 'ANGRY');

CREATE TABLE IF NOT EXISTS support_agents (
    agent_id UUID PRIMARY KEY,
    agent_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS support_sessions (
    session_id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    agent_id UUID,
    session_status support_session_status NOT NULL,
    started_at TIMESTAMP,
    closed_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (agent_id) REFERENCES support_agents(agent_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS support_messages (
    message_id UUID PRIMARY KEY,
    session_id UUID NOT NULL,
    sender support_messages_sender_type NOT NULL,
    reaction_type support_messages_reaction_type NOT NULL DEFAULT 'NONE',
    message_text TEXT,
    sent_at TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES support_sessions(session_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS support_message_attachments (
    attachment_id UUID PRIMARY KEY,
    message_id UUID NOT NULL,
    file_url VARCHAR(255),
    file_type VARCHAR(50),
    uploaded_at TIMESTAMP,
    FOREIGN KEY (message_id) REFERENCES support_messages(message_id) ON DELETE CASCADE
);
