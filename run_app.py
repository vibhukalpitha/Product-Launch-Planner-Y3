#!/usr/bin/env python3
"""
Startup script for Samsung Product Launch Planner
Run this script to start the Streamlit application
"""
import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {platform.python_version()}")
        return False
    
    print(f"✅ Python version: {platform.python_version()}")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["data", "logs"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")

def run_streamlit():
    """Run the Streamlit application"""
    print("🚀 Starting Samsung Product Launch Planner...")
    print("📱 The application will open in your default web browser")
    print("🌐 URL: http://localhost:8501")
    print("\n" + "="*50)
    print("Press Ctrl+C to stop the application")
    print("="*50 + "\n")
    
    try:
        # Change to the project directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "ui/streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    """Main startup function"""
    print("🏢 Samsung Product Launch Planner - Startup Script")
    print("="*55)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        return
    
    # Run the application
    run_streamlit()

if __name__ == "__main__":
    main()