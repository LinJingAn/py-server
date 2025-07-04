@echo off
echo Setting up Activity Simulator for Windows...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Install Windows-specific dependencies
echo Installing Windows-specific dependencies...
pip install pywin32==307

echo Setup complete!
echo To run the simulator:
echo 1. Activate the virtual environment: venv\Scripts\activate.bat
echo 2. Run the simulator: python server.py
pause 