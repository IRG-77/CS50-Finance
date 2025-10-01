import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLite database
def get_db_connection():
    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    db = get_db_connection()
    try:
        # Get user's stocks and cash
        rows = db.execute("""
            SELECT symbol, SUM(shares) as total_shares 
            FROM transactions 
            WHERE user_id = ? 
            GROUP BY symbol 
            HAVING total_shares > 0
        """, (session["user_id"],)).fetchall()
        
        stocks = []
        total_value = 0
        
        for row in rows:
            quote = lookup(row["symbol"])
            if quote:
                stock_value = row["total_shares"] * quote["price"]
                stocks.append({
                    "symbol": row["symbol"],
                    "shares": row["total_shares"],
                    "price": quote["price"],
                    "total": stock_value
                })
                total_value += stock_value
        
        # Get user's cash
        cash_row = db.execute("SELECT cash FROM users WHERE id = ?", (session["user_id"],)).fetchone()
        cash = cash_row["cash"] if cash_row else 0
        
        return render_template("index.html", stocks=stocks, cash=cash, total_value=total_value + cash)
    finally:
        db.close()

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        
        if not symbol:
            return apology("must provide symbol")
        symbol = symbol.upper()
        if not shares:
            return apology("must provide number of shares")
        try:
            shares = int(shares)
            if shares <= 0:
                return apology("must provide positive number of shares")
        except ValueError:
            return apology("must provide valid number of shares")
        
        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol")
        cost = shares * quote["price"]
        
        db = get_db_connection()
        try:
            # Check if user has enough cash
            if "user_id" not in session:
                return apology("not logged in")
            user_row = db.execute("SELECT cash FROM users WHERE id = ?", (session["user_id"],)).fetchone()
            if not user_row or user_row["cash"] < cost:
                return apology("insufficient funds")
            
            # Update user's cash
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", (cost, session["user_id"]))
            
            # Record transaction
            db.execute("""
                INSERT INTO transactions (user_id, symbol, shares, price, type)
                VALUES (?, ?, ?, ?, 'buy')
            """, (session["user_id"], symbol, shares, quote["price"]))
            
            db.commit()
            flash("Bought!")
            return redirect("/")
        except Exception as e:
            db.rollback()
            return apology(f"Database error: {str(e)}")
        finally:
            db.close()
    
    return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    db = get_db_connection()
    try:
        transactions = db.execute("""
            SELECT * FROM transactions 
            WHERE user_id = ? 
            ORDER BY timestamp DESC
        """, (session["user_id"],)).fetchall()
        
        return render_template("history.html", transactions=transactions)
    finally:
        db.close()

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username:
            return apology("must provide username")
        if not password:
            return apology("must provide password")
        
        db = get_db_connection()
        try:
            user_row = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            
            if not user_row or not check_password_hash(user_row["hash"], password):
                return apology("invalid username and/or password")
            
            session["user_id"] = user_row["id"]
        finally:
            db.close()
        flash("Welcome!")
        return redirect("/")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol")
        
        quote_data = lookup(symbol)
        if not quote_data:
            return apology("invalid symbol")
        
        return render_template("quote.html", quote=quote_data)
    
    return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        if not username:
            return apology("must provide username")
        if not password:
            return apology("must provide password")
        if password != confirmation:
            return apology("passwords don't match")
        
        db = get_db_connection()
        try:
            # Check if username already exists
            existing_user = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
            if existing_user:
                return apology("username already exists")
            
            # Insert new user
            hash_password = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash_password))
            db.commit()
        finally:
            db.close()
        
        flash("Registered!")
        return redirect("/login")
    
    return render_template("register.html")

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Allow users to change their password"""
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")
        
        if not current_password:
            return apology("must provide current password")
        if not new_password:
            return apology("must provide new password")
        if new_password != confirmation:
            return apology("new passwords don't match")
        
        db = get_db_connection()
        try:
            # Verify current password
            user_row = db.execute("SELECT hash FROM users WHERE id = ?", (session["user_id"],)).fetchone()
            if not user_row or not check_password_hash(user_row["hash"], current_password):
                return apology("current password is incorrect")
            
            # Update password
            new_hash = generate_password_hash(new_password)
            db.execute("UPDATE users SET hash = ? WHERE id = ?", (new_hash, session["user_id"]))
            db.commit()
            
            flash("Password changed successfully!")
            return redirect("/")
        finally:
            db.close()
    
    return render_template("change_password.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        
        if not symbol:
            return apology("must provide symbol")
        if not shares:
            return apology("must provide number of shares")
        try:
            shares = int(shares)
            if shares <= 0:
                return apology("must provide positive number of shares")
        except ValueError:
            return apology("must provide valid number of shares")
        
        db = get_db_connection()
        try:
            # Check if user owns enough shares
            if "user_id" not in session:
                return apology("not logged in")
            user_shares = db.execute("""
                SELECT SUM(shares) as total_shares 
                FROM transactions 
                WHERE user_id = ? AND symbol = ?
            """, (session["user_id"], symbol)).fetchone()
            
            if not user_shares or user_shares["total_shares"] < shares:
                return apology("insufficient shares")
            
            quote = lookup(symbol)
            if not quote:
                return apology("invalid symbol")
            
            cost = shares * quote["price"]
            
            # Update user's cash
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", (cost, session["user_id"]))
            
            # Record transaction
            db.execute("""
                INSERT INTO transactions (user_id, symbol, shares, price, type)
                VALUES (?, ?, ?, ?, 'sell')
            """, (session["user_id"], symbol, -shares, quote["price"]))
            
            db.commit()
            flash("Sold!")
            return redirect("/")
        except Exception as e:
            db.rollback()
            return apology(f"Database error: {str(e)}")
        finally:
            db.close()
    
    # Get user's stocks for dropdown
    db = get_db_connection()
    try:
        stocks = db.execute("""
            SELECT symbol, SUM(shares) as total_shares 
            FROM transactions 
            WHERE user_id = ? 
            GROUP BY symbol 
            HAVING total_shares > 0
        """, (session["user_id"],)).fetchall()
        
        return render_template("sell.html", stocks=stocks)
    finally:
        db.close()

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run(debug=True)
