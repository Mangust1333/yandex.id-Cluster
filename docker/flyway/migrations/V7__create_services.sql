CREATE TYPE notification_name_type AS ENUM ('CALL', 'PUSH', 'SMS', 'EMAIL', 'OTHER');

CREATE TABLE IF NOT EXISTS notification_types (
    notification_type_id UUID PRIMARY KEY,
    type_name notification_name_type NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS services (
    service_id UUID PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS service_address_notes (
    user_id UUID NOT NULL,
    addresses_id UUID NOT NULL,
    service_id UUID NOT NULL,
    description TEXT,
    PRIMARY KEY (user_id, addresses_id, service_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id, addresses_id) REFERENCES user_addresses(user_id, address_id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES services(service_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS service_notification_types (
    service_notification_type_id UUID PRIMARY KEY,
    service_id UUID NOT NULL,
    notification_type_id UUID NOT NULL,
    FOREIGN KEY (service_id) REFERENCES services(service_id) ON DELETE CASCADE,
    FOREIGN KEY (notification_type_id) REFERENCES notification_types(notification_type_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_service_notification_disabled (
    user_id UUID NOT NULL,
    service_notification_type_id UUID NOT NULL,
    PRIMARY KEY (user_id, service_notification_type_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (service_notification_type_id) REFERENCES service_notification_types(service_notification_type_id) ON DELETE CASCADE
);
