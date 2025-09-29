#!/usr/bin/env python3
"""
Script to prepare C$50 Finance project for submission
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_submission_package():
    """Create a clean submission package"""
    
    print("📦 Preparing C$50 Finance submission package...")
    
    # Create submission directory
    submission_dir = "finance_submission"
    if os.path.exists(submission_dir):
        shutil.rmtree(submission_dir)
    os.makedirs(submission_dir)
    
    # Copy essential files
    essential_files = [
        "app.py",
        "helpers.py", 
        "requirements.txt",
        "finance.db"
    ]
    
    print("📁 Copying essential files...")
    for file in essential_files:
        if os.path.exists(file):
            shutil.copy2(file, submission_dir)
            print(f"✅ Copied: {file}")
        else:
            print(f"⚠️  Missing: {file}")
    
    # Copy templates directory
    if os.path.exists("templates"):
        shutil.copytree("templates", os.path.join(submission_dir, "templates"))
        print("✅ Copied: templates/")
    
    # Copy static directory
    if os.path.exists("static"):
        shutil.copytree("static", os.path.join(submission_dir, "static"))
        print("✅ Copied: static/")
    
    # Create ZIP file
    zip_filename = "finance_submission.zip"
    print(f"\n📦 Creating {zip_filename}...")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(submission_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, submission_dir)
                zipf.write(file_path, arcname)
                print(f"📄 Added: {arcname}")
    
    print(f"\n🎉 Submission package created: {zip_filename}")
    print(f"📁 Package contents:")
    
    # List contents
    with zipfile.ZipFile(zip_filename, 'r') as zipf:
        for file_info in zipf.filelist:
            print(f"  - {file_info.filename}")
    
    print(f"\n📋 Submission checklist:")
    print("✅ app.py - Main Flask application")
    print("✅ helpers.py - Helper functions")
    print("✅ requirements.txt - Dependencies")
    print("✅ templates/ - All HTML templates")
    print("✅ static/ - CSS and assets")
    print("✅ finance.db - Database (optional)")
    
    print(f"\n🚀 Ready for submission!")
    print(f"📤 Upload {zip_filename} to CS50 or use in codespace")

def verify_submission():
    """Verify the submission package"""
    
    print("\n🔍 Verifying submission package...")
    
    required_files = [
        "app.py",
        "helpers.py",
        "requirements.txt",
        "templates/layout.html",
        "templates/index.html",
        "templates/login.html",
        "templates/register.html",
        "templates/quote.html",
        "templates/buy.html",
        "templates/sell.html",
        "templates/history.html",
        "templates/change_password.html",
        "static/styles.css"
    ]
    
    all_present = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            all_present = False
    
    if all_present:
        print("\n🎉 All required files present!")
        return True
    else:
        print("\n⚠️  Some files are missing. Please check the list above.")
        return False

if __name__ == "__main__":
    print("🎯 C$50 Finance - Submission Preparation")
    print("=" * 50)
    
    # Verify current directory has the right files
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found. Please run this script from the finance directory.")
        exit(1)
    
    # Verify files are present
    if verify_submission():
        # Create submission package
        create_submission_package()
        print("\n🎉 Your C$50 Finance project is ready for submission!")
    else:
        print("\n⚠️  Please ensure all required files are present before creating submission package.")
