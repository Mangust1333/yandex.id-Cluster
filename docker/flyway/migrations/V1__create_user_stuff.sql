CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY,
    login VARCHAR(32) UNIQUE NOT NULL,
    avatar TEXT UNIQUE,
    is_premium_user BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS roles (
    role_id UUID PRIMARY KEY,
    role VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS user_roles (
    user_id UUID PRIMARY KEY NOT NULL,
    role_id UUID NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS actions (
    action_id UUID PRIMARY KEY,
    action_name VARCHAR(100) UNIQUE NOT NULL,
    action_description TEXT
);

CREATE TYPE device_type AS ENUM ('SMARTPHONE', 'TABLET', 'PC', 'LAPTOP', 'OTHER');

CREATE TABLE IF NOT EXISTS devices (
    device_id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    device_type device_type NOT NULL,
    device_name VARCHAR(100) NOT NULL,
    os VARCHAR(50) NOT NULL,
    os_version VARCHAR(50),
    last_login TIMESTAMP,
    last_ip VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS activity_history (
    activity_id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    device_id UUID NOT NULL,
    action_id UUID NOT NULL,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (device_id) REFERENCES devices(device_id) ON DELETE CASCADE,
    FOREIGN KEY (action_id) REFERENCES actions(action_id) ON DELETE CASCADE
);

