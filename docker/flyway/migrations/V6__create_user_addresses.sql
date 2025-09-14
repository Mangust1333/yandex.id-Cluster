CREATE TYPE address_type AS ENUM ('HOME', 'WORK', 'OTHER');

CREATE TABLE IF NOT EXISTS addresses (
    address_id UUID PRIMARY KEY,
    name_of_address VARCHAR(20),
    country VARCHAR(100),
    region VARCHAR(100),
    city VARCHAR(100),
    street VARCHAR(100),
    building VARCHAR(10),
    UNIQUE (name_of_address, country, region, city, street, building)
);

CREATE TABLE IF NOT EXISTS user_addresses (
    user_id UUID NOT NULL,
    address_id UUID NOT NULL,
    main_description TEXT,
    address_type address_type NOT NULL,
    entrance VARCHAR(10),
    floor VARCHAR(10),
    apartment VARCHAR(10),
    intercom VARCHAR(10),
    PRIMARY KEY (user_id, address_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (address_id) REFERENCES addresses(address_id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX unique_home_address ON user_addresses(user_id) WHERE address_type = 'HOME';

CREATE UNIQUE INDEX unique_work_address ON user_addresses(user_id) WHERE address_type = 'WORK';