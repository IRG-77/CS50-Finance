import sqlite3
from werkzeug.security import generate_password_hash

# Connect to database
db = sqlite3.connect("finance.db")
db.row_factory = sqlite3.Row

# Create tables if they don't exist
db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL,
        cash NUMERIC NOT NULL DEFAULT 10000.00
    )
""")

db.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        symbol TEXT NOT NULL,
        shares INTEGER NOT NULL,
        price NUMERIC NOT NULL,
        type TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
""")

# Reset users table
db.execute("DELETE FROM users")
db.execute("DELETE FROM transactions")

# Insert default users
users = [
    ("admin", "admin123"),
    ("test", "test123"),
    ("demo", "demo123")
]

for username, password in users:
    hash_password = generate_password_hash(password)
    db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash_password))

db.commit()
db.close()

print("Database reset successfully!")
print("Default users created:")
for username, password in users:
    print(f"  Username: {username}, Password: {password}")
