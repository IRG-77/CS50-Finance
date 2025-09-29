#!/usr/bin/env python3
"""
Database initialization script for C$50 Finance
Creates the necessary tables and indexes
"""

import sqlite3
import os

def init_database():
    """Initialize the database with required tables"""
    
    # Connect to database
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            hash TEXT NOT NULL,
            cash NUMERIC NOT NULL DEFAULT 10000.00
        )
    """)
    
    # Create transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            shares INTEGER NOT NULL,
            price NUMERIC NOT NULL,
            type TEXT NOT NULL CHECK (type IN ('buy', 'sell')),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Create indexes for better performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions (user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_symbol ON transactions (symbol)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_timestamp ON transactions (timestamp)")
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username ON users (username)")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()
