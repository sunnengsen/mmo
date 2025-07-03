@echo off
REM 🚀 Video Tool Pro - Windows Setup Script

echo 🎬 Video Tool Pro - Windows Setup Script
echo ==========================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [SUCCESS] Python found
python --version

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip is not installed!
    pause
    exit /b 1
)

echo [SUCCESS] pip found

REM Check if FFmpeg is installed
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] FFmpeg is not installed!
    echo.
    echo Please install FFmpeg:
    echo 1. Download from https://ffmpeg.org/download.html
    echo 2. Extract to C:\ffmpeg
    echo 3. Add C:\ffmpeg\bin to your PATH
    echo.
    echo Or install using Chocolatey: choco install ffmpeg
    echo.
    pause
    echo Continuing setup without FFmpeg...
) else (
    echo [SUCCESS] FFmpeg found
)

REM Create virtual environment
echo [INFO] Creating virtual environment...
if exist "venv" (
    echo [WARNING] Virtual environment already exists
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip
echo [INFO] Upgrading pip...
pip install --upgrade pip

REM Install requirements
echo [INFO] Installing Python dependencies...
if exist "requirements.txt" (
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install requirements
        pause
        exit /b 1
    )
    echo [SUCCESS] Requirements installed
) else (
    echo [ERROR] requirements.txt not found!
    pause
    exit /b 1
)

REM Install yt-dlp
echo [INFO] Installing yt-dlp...
pip install yt-dlp
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install yt-dlp
    pause
    exit /b 1
)
echo [SUCCESS] yt-dlp installed

REM Test installation
echo [INFO] Testing installation...

REM Test PyQt6
python -c "import PyQt6; print('PyQt6: OK')" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] PyQt6 test failed
    pause
    exit /b 1
)
echo [SUCCESS] PyQt6 test passed

REM Test UI styles
python -c "import ui_styles_new; print('UI Styles: OK')" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] UI Styles test failed
    pause
    exit /b 1
)
echo [SUCCESS] UI Styles test passed

REM Test yt-dlp
yt-dlp --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] yt-dlp test failed
    pause
    exit /b 1
)
echo [SUCCESS] yt-dlp test passed

echo.
echo [SUCCESS] 🎉 Setup completed successfully!
echo.
echo To run the application:
echo   1. Activate virtual environment: venv\Scripts\activate
echo   2. Run the app: python video_tool_app.py
echo   3. Or run with themes: python video_tool_app_themed.py
echo   4. Or test themes: python simple_theme_demo.py
echo.
echo Next steps:
echo   - Read README.md for detailed information
echo   - Check THEME_SWITCHING_README.md for theme features
echo   - Run 'python test_theme.py' to test theme switching
echo.
pause
