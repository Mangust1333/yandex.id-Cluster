CREATE TYPE gender AS ENUM ('MALE', 'FEMALE');

CREATE TABLE IF NOT EXISTS time_zones (
    time_zone_id SMALLINT PRIMARY KEY,
    utc_offset INTERVAL NOT NULL,
    city VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS personal_data_records (
    user_id UUID PRIMARY KEY,
    time_zone_id SMALLINT NOT NULL,
    name VARCHAR(39) NOT NULL,
    surname VARCHAR(39) NOT NULL,
    gender gender NOT NULL,
    birth_date DATE,
    locality VARCHAR(100),
    nickname VARCHAR(39) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (time_zone_id) REFERENCES time_zones(time_zone_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS driver_licenses (
    user_id UUID PRIMARY KEY,
    number CHAR(10) NOT NULL,
    surname VARCHAR(39),
    latin_surname VARCHAR(39),
    name VARCHAR(39),
    latin_name VARCHAR(39),
    patronymic VARCHAR(39),
    latin_patronymic VARCHAR(39),
    birth_date DATE,
    birth_place VARCHAR(50),
    latin_birth_place VARCHAR(50),
    date_of_issue DATE,
    expiration_date DATE,
    issued_by_whom VARCHAR(100),
    issued_by_whom_latin VARCHAR(100),
    issue_place VARCHAR(100),
    issue_place_latin VARCHAR(100),
    categories VARCHAR(3) NOT NULL,
    special_marks VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS driver_license_categories (
    driver_license_user_id UUID NOT NULL,
    category VARCHAR(5) NOT NULL,
    PRIMARY KEY (driver_license_user_id, category),
    FOREIGN KEY (driver_license_user_id) REFERENCES driver_licenses(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS international_passports (
    user_id UUID PRIMARY KEY,
    number CHAR(9) NOT NULL,
    surname VARCHAR(39),
    latin_surname VARCHAR(39),
    name VARCHAR(39),
    latin_name VARCHAR(39),
    patronymic VARCHAR(39),
    latin_patronymic VARCHAR(39),
    nationality VARCHAR(50),
    latin_nationality VARCHAR(50),
    birth_date DATE,
    birth_place VARCHAR(50),
    latin_birth_place VARCHAR(50),
    gender gender,
    date_of_issue DATE,
    expiration_date DATE,
    issued_by_whom VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS compulsory_medical_insurances (
    user_id UUID PRIMARY KEY,
    number CHAR(16) NOT NULL,
    surname VARCHAR(39),
    name VARCHAR(39),
    patronymic VARCHAR(39),
    birth_date DATE,
    gender gender,
    blank_number CHAR(4),
    blank_seria CHAR(7),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS birth_certificates (
    user_id UUID PRIMARY KEY,
    seria CHAR(2) NOT NULL,
    number CHAR(6) NOT NULL,
    name VARCHAR(39),
    surname VARCHAR(39),
    patronymic VARCHAR(39),
    birth_date DATE,
    birth_place VARCHAR(50),
    birth_certificate_record_number CHAR(21),
    father_name VARCHAR(39),
    father_surname VARCHAR(39),
    father_patronymic VARCHAR(39),
    father_birth_date DATE,
    father_nationality VARCHAR(50),
    mother_name VARCHAR(39),
    mother_surname VARCHAR(39),
    mother_patronymic VARCHAR(39),
    mother_birth_date DATE,
    mother_nationality VARCHAR(50),
    state_registration_place VARCHAR(50),
    issue_certificate_place VARCHAR(50),
    date_of_issue DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS voluntary_medical_insurances (
    user_id UUID PRIMARY KEY,
    number CHAR(16) NOT NULL,
    surname VARCHAR(39),
    name VARCHAR(39),
    patronymic VARCHAR(39),
    birth_date DATE,
    gender gender,
    date_of_issue DATE,
    expiration_date DATE,
    insurer VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS vehicle_registration_certificates (
    user_id UUID PRIMARY KEY,
    seria CHAR(4) NOT NULL,
    number CHAR(6) NOT NULL,
    registration_number CHAR(8),
    vin CHAR(17),
    brand VARCHAR(50),
    brand_latin VARCHAR(50),
    model VARCHAR(50),
    model_latin VARCHAR(50),
    vehicle_type VARCHAR(50),
    vehicle_category VARCHAR(50),
    manufacture_year SMALLINT,
    chassis_number VARCHAR(17),
    body_number VARCHAR(17),
    color VARCHAR(20),
    engine_power_kw FLOAT,
    engine_power_hp FLOAT,
    ec_class VARCHAR(20),
    max_allowed_weight FLOAT,
    curb_weight FLOAT,
    registration_expiration_date DATE,
    pts_number CHAR(15),
    surname VARCHAR(39),
    surname_latin VARCHAR(39),
    name VARCHAR(39),
    name_latin VARCHAR(39),
    patronymic VARCHAR(39),
    registration_address VARCHAR(100),
    subdivision_code CHAR(6),
    issue_date DATE,
    special_marks VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS social_insurance_numbers (
    user_id UUID PRIMARY KEY,
    snils CHAR(11) NOT NULL,
    surname VARCHAR(39),
    name VARCHAR(50),
    patronymic VARCHAR(50),
    birth_date DATE,
    gender gender,
    registration_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS taxpayer_identification_numbers (
    user_id UUID PRIMARY KEY,
    inn CHAR(12) NOT NULL,
    surname VARCHAR(39),
    name VARCHAR(39),
    patronymic VARCHAR(39),
    birth_date DATE,
    place_of_birth VARCHAR(50),
    gender gender,
    issuing_authority VARCHAR(100),
    date_of_issue DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS passports (
    user_id UUID PRIMARY KEY,
    seria CHAR(4) NOT NULL,
    number CHAR(6) NOT NULL,
    name VARCHAR(39),
    surname VARCHAR(39),
    patronymic VARCHAR(39),
    birth_date DATE,
    locality VARCHAR(100),
    gender gender,
    issued_by_whom VARCHAR(100),
    unit_code CHAR(6),
    date_of_issue DATE,
    registration_address VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
