@echo off
echo 🏢 Samsung Product Launch Planner - Windows Startup
echo ===================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Install requirements
echo 📦 Installing required packages...
python -m pip install --upgrade pip
python -m pip install streamlit pandas numpy plotly requests python-dateutil scikit-learn
if errorlevel 1 (
    echo ❌ Error installing packages
    pause
    exit /b 1
)

REM Create necessary directories
if not exist "data" mkdir data
if not exist "logs" mkdir logs

REM Run the application
echo 🚀 Starting Samsung Product Launch Planner...
echo 📱 The application will open in your default web browser
echo 🌐 URL: http://localhost:8501
echo.
echo ==================================================
echo Press Ctrl+C to stop the application
echo ==================================================
echo.

python -m streamlit run ui/streamlit_app.py --server.port 8501 --server.address localhost

pause