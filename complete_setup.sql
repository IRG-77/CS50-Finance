-- C$50 Finance Complete Database Setup
-- Run this script to create and populate the database

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    cash NUMERIC NOT NULL DEFAULT 10000.00
);

-- Create transactions table
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL,
    price NUMERIC NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('buy', 'sell')),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Create indexes for performance
CREATE INDEX idx_transactions_user_id ON transactions (user_id);
CREATE INDEX idx_transactions_symbol ON transactions (symbol);
CREATE INDEX idx_transactions_timestamp ON transactions (timestamp);
CREATE UNIQUE INDEX idx_users_username ON users (username);

-- Insert sample users with hashed passwords
-- Note: These are example hashes. In production, use proper password hashing
INSERT INTO users (username, hash, cash) VALUES 
('alice', 'pbkdf2:sha256:260000$example$hash1', 10000.00),
('bob', 'pbkdf2:sha256:260000$example$hash2', 10000.00),
('charlie', 'pbkdf2:sha256:260000$example$hash3', 10000.00),
('diana', 'pbkdf2:sha256:260000$example$hash4', 10000.00),
('eve', 'pbkdf2:sha256:260000$example$hash5', 10000.00);

-- Insert sample transactions
INSERT INTO transactions (user_id, symbol, shares, price, type, timestamp) VALUES
-- Alice's transactions
(1, 'AAPL', 10, 150.00, 'buy', '2024-01-15 10:30:00'),
(1, 'GOOGL', 5, 2800.00, 'buy', '2024-01-16 14:20:00'),
(1, 'AAPL', 5, 155.00, 'sell', '2024-01-20 09:15:00'),
(1, 'MSFT', 15, 300.00, 'buy', '2024-01-22 11:30:00'),

-- Bob's transactions
(2, 'MSFT', 20, 300.00, 'buy', '2024-01-18 11:45:00'),
(2, 'AMZN', 3, 3200.00, 'buy', '2024-01-19 16:30:00'),
(2, 'TSLA', 10, 800.00, 'buy', '2024-01-21 13:20:00'),
(2, 'MSFT', 5, 310.00, 'sell', '2024-01-23 10:15:00'),

-- Charlie's transactions
(3, 'TSLA', 15, 800.00, 'buy', '2024-01-17 13:20:00'),
(3, 'META', 25, 350.00, 'buy', '2024-01-21 10:10:00'),
(3, 'NVDA', 8, 400.00, 'buy', '2024-01-24 14:45:00'),
(3, 'TSLA', 5, 820.00, 'sell', '2024-01-25 09:30:00'),

-- Diana's transactions
(4, 'GOOGL', 10, 2800.00, 'buy', '2024-01-20 15:30:00'),
(4, 'NFLX', 8, 450.00, 'buy', '2024-01-22 12:20:00'),
(4, 'AAPL', 12, 155.00, 'buy', '2024-01-24 16:10:00'),

-- Eve's transactions
(5, 'AMZN', 5, 3200.00, 'buy', '2024-01-19 14:20:00'),
(5, 'MSFT', 15, 305.00, 'buy', '2024-01-21 11:45:00'),
(5, 'GOOGL', 3, 2850.00, 'buy', '2024-01-23 13:15:00'),
(5, 'AMZN', 2, 3250.00, 'sell', '2024-01-25 10:30:00');

-- Update cash balances based on transactions
-- This is a simplified calculation - in practice, you'd want more sophisticated logic
UPDATE users SET cash = 10000.00 - (
    SELECT COALESCE(SUM(CASE WHEN type = 'buy' THEN shares * price ELSE 0 END), 0)
    FROM transactions 
    WHERE transactions.user_id = users.id
) + (
    SELECT COALESCE(SUM(CASE WHEN type = 'sell' THEN shares * price ELSE 0 END), 0)
    FROM transactions 
    WHERE transactions.user_id = users.id
);

-- Display final results
SELECT 'Database setup complete!' as status;
SELECT 'Users created:' as info, COUNT(*) as count FROM users;
SELECT 'Transactions created:' as info, COUNT(*) as count FROM transactions;

-- Show user balances
SELECT username, cash FROM users ORDER BY username;

-- Show portfolio summary
SELECT 
    u.username,
    t.symbol,
    SUM(t.shares) as total_shares,
    AVG(t.price) as avg_price
FROM users u
JOIN transactions t ON u.id = t.user_id
GROUP BY u.id, u.username, t.symbol
HAVING total_shares > 0
ORDER BY u.username, t.symbol;
