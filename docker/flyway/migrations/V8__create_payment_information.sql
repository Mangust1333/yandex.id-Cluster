CREATE TYPE payment_system AS ENUM ('VISA', 'MASTERCARD', 'MIR', 'AMEX', 'JCB', 'UNIONPAY');
CREATE TYPE transaction_status AS ENUM ('PENDING', 'SUCCESS', 'FAILED', 'CANCELED');
CREATE TYPE transaction_type AS ENUM ('PAYMENT', 'REFUND');

CREATE TABLE IF NOT EXISTS bank_cards (
    bank_card_id CHAR(16) PRIMARY KEY,
    user_id UUID NOT NULL,
    cardholder_name VARCHAR(100),
    expiration_date DATE,
    payment_system payment_system NOT NULL,
    bank_name VARCHAR(100),
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (bank_card_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    bank_card_id CHAR(16) NOT NULL,
    service_id UUID NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency CHAR(3) NOT NULL,
    status transaction_status NOT NULL,
    transaction_type transaction_type NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    receipt VARCHAR(100) UNIQUE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (bank_card_id) REFERENCES bank_cards(bank_card_id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES services(service_id) ON DELETE SET NULL
);
