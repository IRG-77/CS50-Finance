#!/usr/bin/env python3
"""
Database population script for C$50 Finance
Adds sample users and transactions for testing
"""

import sqlite3
from werkzeug.security import generate_password_hash
import random
from datetime import datetime, timedelta

def populate_database():
    """Populate database with sample data"""
    
    # Connect to database
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # Sample users
    users = [
        ("alice", "password123"),
        ("bob", "password456"),
        ("charlie", "password789"),
        ("diana", "password101"),
        ("eve", "password202")
    ]
    
    # Sample stock symbols and prices
    stocks = [
        ("AAPL", 150.0),
        ("GOOGL", 2800.0),
        ("MSFT", 300.0),
        ("AMZN", 3200.0),
        ("TSLA", 800.0),
        ("META", 350.0),
        ("NVDA", 400.0),
        ("NFLX", 450.0)
    ]
    
    print("Adding sample users...")
    for username, password in users:
        try:
            hash_password = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO users (username, hash, cash) VALUES (?, ?, ?)",
                (username, hash_password, 10000.00)
            )
            print(f"Added user: {username}")
        except sqlite3.IntegrityError:
            print(f"User {username} already exists, skipping...")
    
    # Get user IDs
    cursor.execute("SELECT id, username FROM users")
    user_data = cursor.fetchall()
    
    print("\nAdding sample transactions...")
    # Add sample transactions for each user
    for user_id, username in user_data:
        # Random number of transactions per user (3-8)
        num_transactions = random.randint(3, 8)
        
        for _ in range(num_transactions):
            # Random stock
            symbol, base_price = random.choice(stocks)
            
            # Random price variation (±20%)
            price_variation = random.uniform(0.8, 1.2)
            price = round(base_price * price_variation, 2)
            
            # Random number of shares (1-10)
            shares = random.randint(1, 10)
            
            # Random transaction type (70% buy, 30% sell)
            transaction_type = "buy" if random.random() < 0.7 else "sell"
            
            # Random timestamp within last 30 days
            days_ago = random.randint(0, 30)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            timestamp = datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
            
            # For sell transactions, make sure user has enough shares
            if transaction_type == "sell":
                # Check current shares for this symbol
                cursor.execute("""
                    SELECT SUM(shares) FROM transactions 
                    WHERE user_id = ? AND symbol = ?
                """, (user_id, symbol))
                result = cursor.fetchone()
                current_shares = result[0] if result[0] else 0
                
                if current_shares < shares:
                    shares = max(1, current_shares)
                    if shares == 0:
                        continue  # Skip if no shares to sell
            
            # Insert transaction
            cursor.execute("""
                INSERT INTO transactions (user_id, symbol, shares, price, type, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, symbol, shares, price, transaction_type, timestamp))
            
            # Update user's cash based on transaction
            if transaction_type == "buy":
                cost = shares * price
                cursor.execute("UPDATE users SET cash = cash - ? WHERE id = ?", (cost, user_id))
            else:  # sell
                revenue = shares * price
                cursor.execute("UPDATE users SET cash = cash + ? WHERE id = ?", (revenue, user_id))
    
    # Commit all changes
    conn.commit()
    
    # Display summary
    print("\nDatabase populated successfully!")
    print("\nSummary:")
    
    # Count users
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    print(f"Users: {user_count}")
    
    # Count transactions
    cursor.execute("SELECT COUNT(*) FROM transactions")
    transaction_count = cursor.fetchone()[0]
    print(f"Transactions: {transaction_count}")
    
    # Show user balances
    print("\nUser balances:")
    cursor.execute("SELECT username, cash FROM users")
    for username, cash in cursor.fetchall():
        print(f"{username}: ${cash:.2f}")
    
    # Show portfolio summary
    print("\nPortfolio summary:")
    cursor.execute("""
        SELECT u.username, t.symbol, SUM(t.shares) as total_shares
        FROM users u
        JOIN transactions t ON u.id = t.user_id
        GROUP BY u.id, u.username, t.symbol
        HAVING total_shares > 0
        ORDER BY u.username, t.symbol
    """)
    
    current_user = None
    for username, symbol, shares in cursor.fetchall():
        if username != current_user:
            print(f"\n{username}:")
            current_user = username
        print(f"  {symbol}: {shares} shares")
    
    conn.close()

if __name__ == "__main__":
    populate_database()
