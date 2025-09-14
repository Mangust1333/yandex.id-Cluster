CREATE TYPE family_group_role AS ENUM ('ADMIN', 'ADULT', 'CHILD');

CREATE TABLE IF NOT EXISTS family_groups (
    group_id UUID PRIMARY KEY,
    group_name VARCHAR(100),
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS family_group_members (
    user_id UUID NOT NULL,
    group_id UUID NOT NULL,
    role family_group_role NOT NULL,
    added_at TIMESTAMP,
    PRIMARY KEY (user_id, group_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES family_groups(group_id) ON DELETE CASCADE
);
