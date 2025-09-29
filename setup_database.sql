-- C$50 Finance Database Setup Script
-- This script creates the database schema and populates it with sample data

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    cash NUMERIC NOT NULL DEFAULT 10000.00
);

-- Create transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL,
    price NUMERIC NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('buy', 'sell')),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions (user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_symbol ON transactions (symbol);
CREATE INDEX IF NOT EXISTS idx_transactions_timestamp ON transactions (timestamp);
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username ON users (username);

-- Insert sample users (passwords are hashed versions of 'password123')
INSERT OR IGNORE INTO users (username, hash, cash) VALUES 
('alice', 'pbkdf2:sha256:260000$example$hash1', 10000.00),
('bob', 'pbkdf2:sha256:260000$example$hash2', 10000.00),
('charlie', 'pbkdf2:sha256:260000$example$hash3', 10000.00);

-- Insert sample transactions
INSERT OR IGNORE INTO transactions (user_id, symbol, shares, price, type, timestamp) VALUES
(1, 'AAPL', 10, 150.00, 'buy', '2024-01-15 10:30:00'),
(1, 'GOOGL', 5, 2800.00, 'buy', '2024-01-16 14:20:00'),
(1, 'AAPL', 5, 155.00, 'sell', '2024-01-20 09:15:00'),
(2, 'MSFT', 20, 300.00, 'buy', '2024-01-18 11:45:00'),
(2, 'AMZN', 3, 3200.00, 'buy', '2024-01-19 16:30:00'),
(3, 'TSLA', 15, 800.00, 'buy', '2024-01-17 13:20:00'),
(3, 'META', 25, 350.00, 'buy', '2024-01-21 10:10:00');

-- Update user cash balances based on transactions
UPDATE users SET cash = cash - (SELECT SUM(shares * price) FROM transactions WHERE user_id = users.id AND type = 'buy') + (SELECT SUM(shares * price) FROM transactions WHERE user_id = users.id AND type = 'sell');
