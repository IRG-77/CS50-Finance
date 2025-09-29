-- C$50 Finance Database Commands
-- Useful SQL commands for managing the finance database

-- View all users and their cash balances
SELECT id, username, cash FROM users ORDER BY username;

-- View all transactions for a specific user
SELECT * FROM transactions WHERE user_id = 1 ORDER BY timestamp DESC;

-- View current portfolio for a specific user
SELECT 
    symbol,
    SUM(shares) as total_shares,
    AVG(price) as avg_price,
    SUM(shares * price) as total_value
FROM transactions 
WHERE user_id = 1 
GROUP BY symbol 
HAVING total_shares > 0
ORDER BY symbol;

-- View transaction history for all users
SELECT 
    u.username,
    t.symbol,
    t.shares,
    t.price,
    t.type,
    t.timestamp
FROM transactions t
JOIN users u ON t.user_id = u.id
ORDER BY t.timestamp DESC;

-- Calculate total portfolio value for each user
SELECT 
    u.username,
    u.cash,
    COALESCE(SUM(t.shares * t.price), 0) as stock_value,
    u.cash + COALESCE(SUM(t.shares * t.price), 0) as total_value
FROM users u
LEFT JOIN transactions t ON u.id = t.user_id
GROUP BY u.id, u.username, u.cash
ORDER BY total_value DESC;

-- Find users with negative cash balance
SELECT username, cash FROM users WHERE cash < 0;

-- Find most traded stocks
SELECT 
    symbol,
    COUNT(*) as transaction_count,
    SUM(ABS(shares)) as total_shares_traded
FROM transactions 
GROUP BY symbol 
ORDER BY transaction_count DESC;

-- Find recent transactions (last 7 days)
SELECT 
    u.username,
    t.symbol,
    t.shares,
    t.price,
    t.type,
    t.timestamp
FROM transactions t
JOIN users u ON t.user_id = u.id
WHERE t.timestamp >= datetime('now', '-7 days')
ORDER BY t.timestamp DESC;

-- Reset a user's cash to $10,000
-- UPDATE users SET cash = 10000.00 WHERE username = 'alice';

-- Delete all transactions for a user
-- DELETE FROM transactions WHERE user_id = 1;

-- Add a new user
-- INSERT INTO users (username, hash, cash) VALUES ('newuser', 'hashed_password', 10000.00);

-- View database schema
-- .schema

-- Export data to CSV
-- .mode csv
-- .output users.csv
-- SELECT * FROM users;
-- .output transactions.csv
-- SELECT * FROM transactions;
