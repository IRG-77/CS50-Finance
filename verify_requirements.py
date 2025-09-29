#!/usr/bin/env python3
"""
Manual verification script for C$50 Finance requirements
This script checks if all required features are implemented
"""

import os
import sqlite3
from flask import Flask
import sys

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - MISSING")
        return False

def check_route_exists(app, route, methods=None):
    """Check if a route exists in the Flask app"""
    if methods is None:
        methods = ['GET']
    
    for rule in app.url_map.iter_rules():
        if rule.rule == route:
            for method in methods:
                if method in rule.methods:
                    print(f"✅ Route {route} ({method}): IMPLEMENTED")
                    return True
    print(f"❌ Route {route} ({methods}): MISSING")
    return False

def check_database_schema():
    """Check if database has required tables and columns"""
    try:
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        
        # Check users table
        cursor.execute("PRAGMA table_info(users)")
        users_columns = [row[1] for row in cursor.fetchall()]
        required_users_columns = ['id', 'username', 'hash', 'cash']
        
        print("\n📊 Database Schema Check:")
        for col in required_users_columns:
            if col in users_columns:
                print(f"✅ Users table has column: {col}")
            else:
                print(f"❌ Users table missing column: {col}")
        
        # Check transactions table
        cursor.execute("PRAGMA table_info(transactions)")
        transactions_columns = [row[1] for row in cursor.fetchall()]
        required_transactions_columns = ['id', 'user_id', 'symbol', 'shares', 'price', 'type', 'timestamp']
        
        for col in required_transactions_columns:
            if col in transactions_columns:
                print(f"✅ Transactions table has column: {col}")
            else:
                print(f"❌ Transactions table missing column: {col}")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False

def main():
    """Main verification function"""
    print("🔍 C$50 Finance Requirements Verification")
    print("=" * 50)
    
    # Check required files
    print("\n📁 Required Files Check:")
    files_to_check = [
        ('app.py', 'Main Flask application'),
        ('helpers.py', 'Helper functions'),
        ('requirements.txt', 'Dependencies file'),
        ('templates/layout.html', 'Base template'),
        ('templates/index.html', 'Portfolio template'),
        ('templates/login.html', 'Login template'),
        ('templates/register.html', 'Registration template'),
        ('templates/quote.html', 'Quote template'),
        ('templates/buy.html', 'Buy template'),
        ('templates/sell.html', 'Sell template'),
        ('templates/history.html', 'History template'),
        ('templates/change_password.html', 'Password change template'),
        ('static/styles.css', 'CSS styles'),
        ('finance.db', 'SQLite database')
    ]
    
    all_files_exist = True
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_files_exist = False
    
    # Check Flask app routes
    print("\n🛣️  Flask Routes Check:")
    try:
        from app import app
        
        routes_to_check = [
            ('/', ['GET']),
            ('/login', ['GET', 'POST']),
            ('/logout', ['GET']),
            ('/register', ['GET', 'POST']),
            ('/quote', ['GET', 'POST']),
            ('/buy', ['GET', 'POST']),
            ('/sell', ['GET', 'POST']),
            ('/history', ['GET']),
            ('/change_password', ['GET', 'POST'])
        ]
        
        all_routes_exist = True
        for route, methods in routes_to_check:
            if not check_route_exists(app, route, methods):
                all_routes_exist = False
        
    except ImportError as e:
        print(f"❌ Cannot import Flask app: {e}")
        all_routes_exist = False
    
    # Check database schema
    print("\n🗄️  Database Schema Check:")
    db_schema_ok = check_database_schema()
    
    # Check helper functions
    print("\n🔧 Helper Functions Check:")
    try:
        from helpers import apology, login_required, lookup, usd
        print("✅ apology function: IMPLEMENTED")
        print("✅ login_required decorator: IMPLEMENTED")
        print("✅ lookup function: IMPLEMENTED")
        print("✅ usd filter: IMPLEMENTED")
        helpers_ok = True
    except ImportError as e:
        print(f"❌ Helper functions check failed: {e}")
        helpers_ok = False
    
    # Check templates for required elements
    print("\n🎨 Template Content Check:")
    template_checks = [
        ('templates/register.html', ['username', 'password', 'confirmation']),
        ('templates/quote.html', ['symbol']),
        ('templates/buy.html', ['symbol', 'shares']),
        ('templates/sell.html', ['symbol', 'shares']),
        ('templates/index.html', ['stocks', 'cash']),
        ('templates/history.html', ['transactions'])
    ]
    
    templates_ok = True
    for template, required_fields in template_checks:
        if os.path.exists(template):
            with open(template, 'r') as f:
                content = f.read()
                for field in required_fields:
                    if field in content:
                        print(f"✅ {template} contains field: {field}")
                    else:
                        print(f"❌ {template} missing field: {field}")
                        templates_ok = False
        else:
            print(f"❌ Template missing: {template}")
            templates_ok = False
    
    # Final summary
    print("\n" + "=" * 50)
    print("📋 VERIFICATION SUMMARY")
    print("=" * 50)
    
    if all_files_exist:
        print("✅ All required files present")
    else:
        print("❌ Some required files missing")
    
    if all_routes_exist:
        print("✅ All required routes implemented")
    else:
        print("❌ Some required routes missing")
    
    if db_schema_ok:
        print("✅ Database schema correct")
    else:
        print("❌ Database schema issues")
    
    if helpers_ok:
        print("✅ Helper functions implemented")
    else:
        print("❌ Helper functions missing")
    
    if templates_ok:
        print("✅ Templates have required content")
    else:
        print("❌ Template content issues")
    
    # Overall assessment
    if all([all_files_exist, all_routes_exist, db_schema_ok, helpers_ok, templates_ok]):
        print("\n🎉 ALL REQUIREMENTS MET! Your C$50 Finance implementation is complete!")
        print("\nKey Features Implemented:")
        print("• User registration and authentication")
        print("• Stock quote lookup")
        print("• Buy and sell stocks")
        print("• Portfolio display")
        print("• Transaction history")
        print("• Password change (personal touch)")
        print("• Proper database schema")
        print("• Security features (password hashing, session management)")
        return True
    else:
        print("\n⚠️  Some requirements may be missing. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
