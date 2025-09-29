# C$50 Finance

A web application for managing stock portfolios, built with Flask and SQLite.

## Features

- **User Registration & Authentication**: Secure user registration and login system
- **Stock Quotes**: Look up real-time stock prices using IEX API
- **Buy Stocks**: Purchase shares of stocks with cash balance tracking
- **Sell Stocks**: Sell owned shares and update cash balance
- **Portfolio View**: Display current holdings, cash balance, and total portfolio value
- **Transaction History**: View all buy/sell transactions with timestamps
- **Password Management**: Change password functionality
- **Responsive Design**: Mobile-friendly interface with Bootstrap styling

## Requirements

- Python 3.7+
- Flask 2.3.3
- Flask-Session 0.5.0
- requests 2.31.0
- Werkzeug 2.3.7

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize the database:
```bash
python init_db.py
```

3. (Optional) Populate with sample data:
```bash
python populate_db.py
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. Register a new account or use existing sample accounts:
   - alice / password123
   - bob / password123
   - charlie / password123

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `hash`: Hashed password
- `cash`: Available cash balance (default: $10,000)

### Transactions Table
- `id`: Primary key
- `user_id`: Foreign key to users table
- `symbol`: Stock symbol
- `shares`: Number of shares (positive for buy, negative for sell)
- `price`: Price per share at time of transaction
- `type`: Transaction type ('buy' or 'sell')
- `timestamp`: When the transaction occurred

## API Integration

The application uses the IEX Cloud API for real-time stock quotes. To use real data:

1. Sign up for a free IEX Cloud account
2. Get your API key
3. Set the environment variable:
```bash
export API_KEY=your_api_key_here
```

Without an API key, the application will use mock data for testing.

## File Structure

```
finance/
├── app.py                 # Main Flask application
├── helpers.py            # Helper functions (lookup, authentication)
├── init_db.py            # Database initialization script
├── populate_db.py        # Sample data population script
├── setup_database.sql    # SQL schema and sample data
├── requirements.txt      # Python dependencies
├── finance.db            # SQLite database
├── static/
│   ├── styles.css        # CSS styling
│   └── favicon.ico       # Site icon
└── templates/
    ├── layout.html       # Base template
    ├── index.html        # Portfolio page
    ├── login.html        # Login form
    ├── register.html     # Registration form
    ├── quote.html        # Stock quote form
    ├── buy.html          # Buy stocks form
    ├── sell.html         # Sell stocks form
    ├── history.html      # Transaction history
    └── change_password.html # Password change form
```

## Features Implemented

✅ **Register**: User registration with validation
✅ **Quote**: Stock price lookup
✅ **Buy**: Purchase stocks with cash validation
✅ **Index**: Portfolio summary with current values
✅ **Sell**: Sell owned stocks
✅ **History**: Complete transaction history
✅ **Personal Touch**: Password change functionality

## Security Features

- Password hashing using Werkzeug
- Session management with Flask-Session
- SQL injection prevention with parameterized queries
- Input validation and sanitization
- Login required decorator for protected routes

## Testing

The application includes sample data for testing:
- Multiple users with different portfolios
- Various stock transactions
- Realistic cash balances and holdings

## License

This project is part of the CS50 course curriculum.
