@echo off
REM 🚀 Quick Fix Script for Virtual Environment Issues
REM This script fixes common virtual environment problems

echo.
echo ========================================
echo 🔧 Virtual Environment Quick Fix
echo ========================================
echo.

REM Check if we're in a virtual environment
if defined VIRTUAL_ENV (
    echo [INFO] Currently in virtual environment: %VIRTUAL_ENV%
    echo [INFO] Deactivating to create fresh environment...
    deactivate
)

REM Remove broken virtual environment
if exist "venv" (
    echo [INFO] Removing broken virtual environment...
    rmdir /s /q venv
    echo [SUCCESS] ✅ Old environment removed
)

REM Check if Python is available
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] ❌ Python not found in PATH!
    echo.
    echo Please install Python first:
    echo 1. Go to https://www.python.org/downloads/
    echo 2. Download Python 3.8 or higher
    echo 3. During installation, CHECK "Add Python to PATH"
    echo 4. Restart Command Prompt and try again
    echo.
    pause
    exit /b 1
) else (
    echo [SUCCESS] ✅ Python found
    python --version
)

REM Create new virtual environment
echo [INFO] Creating fresh virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] ❌ Failed to create virtual environment
    pause
    exit /b 1
) else (
    echo [SUCCESS] ✅ Virtual environment created
)

REM Activate the new environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] ❌ Failed to activate virtual environment
    pause
    exit /b 1
) else (
    echo [SUCCESS] ✅ Virtual environment activated
)

REM Install basic requirements
echo [INFO] Installing basic requirements...
python -m pip install --upgrade pip --quiet
pip install PyQt6 yt-dlp --quiet
if %errorlevel% neq 0 (
    echo [ERROR] ❌ Failed to install basic requirements
    pause
    exit /b 1
) else (
    echo [SUCCESS] ✅ Basic requirements installed
)

echo.
echo ========================================
echo [SUCCESS] 🎉 Quick Fix Completed!
echo ========================================
echo.
echo ✅ Virtual environment recreated successfully
echo ✅ Basic packages installed
echo.
echo 🚀 Next steps:
echo    1. You should now see (venv) in your prompt
echo    2. Run: python app.py
echo    3. Or run the full setup: setup.bat
echo.
pause
