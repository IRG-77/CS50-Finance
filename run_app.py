#!/usr/bin/env python3
"""
Simple script to run the C$50 Finance application
"""

import os
import sys
from app import app

if __name__ == "__main__":
    # Set environment variables for development
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    
    print("Starting C$50 Finance application...")
    print("Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
