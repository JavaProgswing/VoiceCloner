@echo off

REM Check if env311 exists, create if it doesn't
if not exist "env311\" (
    echo Creating virtual environment env311...
    python -m venv env311
    if errorlevel 1 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate the virtual environment
call env311\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

REM Run PyInstaller
echo Building executable...
python -O -m PyInstaller voice_server.spec