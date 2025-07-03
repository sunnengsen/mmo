@echo off
REM 🚀 Video Tool Pro - Windows Setup Script
REM Enhanced version with better error handling and user guidance

echo.
echo ========================================
echo 🎬 Video Tool Pro - Windows Setup
echo ========================================
echo.

REM Check if Python is installed
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo ❌ Python not found. Please install Python first:
    echo    1. Go to https://www.python.org/downloads/
    echo    2. Download Python 3.8 or higher
    echo    3. During installation, CHECK "Add Python to PATH"
    echo    4. Restart Command Prompt and try again
    echo.
    pause
    exit /b 1
) else (
    echo [SUCCESS] ✅ Python found
    python --version
)

REM Check if pip is installed
echo [INFO] Checking pip installation...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip is not installed!
    echo.
    echo ❌ pip not found. Usually comes with Python.
    echo    Try: python -m pip --version
    echo.
    pause
    exit /b 1
) else (
    echo [SUCCESS] ✅ pip found
)

REM Check if FFmpeg is installed
echo [INFO] Checking FFmpeg installation...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] ⚠️  FFmpeg is not installed!
    echo.
    echo FFmpeg is needed for video processing. Install options:
    echo    1. Chocolatey: choco install ffmpeg
    echo    2. winget: winget install ffmpeg  
    echo    3. Manual: Download from https://ffmpeg.org/download.html
    echo.
    echo ℹ️  Setup will continue, but video processing may not work.
    pause
) else (
    echo [SUCCESS] ✅ FFmpeg found
)

REM Create virtual environment
echo.
echo [INFO] Creating virtual environment...
if exist "venv" (
    echo [WARNING] ⚠️  Virtual environment already exists
    echo    Removing old environment...
    rmdir /s /q venv
)

python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] ❌ Failed to create virtual environment
    echo    Make sure Python is properly installed
    pause
    exit /b 1
) else (
    echo [SUCCESS] ✅ Virtual environment created
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] ❌ Failed to activate virtual environment
    pause
    exit /b 1
) else (
    echo [SUCCESS] ✅ Virtual environment activated
)

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip --quiet
if %errorlevel% neq 0 (
    echo [WARNING] ⚠️  Failed to upgrade pip, continuing anyway...
)

REM Install requirements
echo [INFO] Installing Python dependencies...
if exist "requirements.txt" (
    pip install -r requirements.txt --quiet
    if %errorlevel% neq 0 (
        echo [ERROR] ❌ Failed to install requirements
        echo    Check your internet connection and try again
        pause
        exit /b 1
    ) else (
        echo [SUCCESS] ✅ Requirements installed
    )
) else (
    echo [ERROR] ❌ requirements.txt not found!
    echo    Make sure you're in the correct project folder
    pause
    exit /b 1
)

REM Install yt-dlp
echo [INFO] Installing yt-dlp (video downloader)...
pip install yt-dlp --quiet
if %errorlevel% neq 0 (
    echo [ERROR] ❌ Failed to install yt-dlp
    pause
    exit /b 1
) else (
    echo [SUCCESS] ✅ yt-dlp installed
)

REM Test installation
echo.
echo [INFO] Testing installation...

REM Test PyQt6
echo [INFO] Testing PyQt6...
python -c "import PyQt6; print('PyQt6: OK')" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] ❌ PyQt6 test failed
    pause
    exit /b 1
) else (
    echo [SUCCESS] ✅ PyQt6 working
)

REM Test UI styles
echo [INFO] Testing theme system...
python -c "import ui_styles_new; print('Theme system: OK')" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] ❌ Theme system test failed
    pause
    exit /b 1
) else (
    echo [SUCCESS] ✅ Theme system working
)

REM Test yt-dlp
echo [INFO] Testing video downloader...
yt-dlp --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] ❌ yt-dlp test failed
    pause
    exit /b 1
) else (
    echo [SUCCESS] ✅ Video downloader working
)

echo.
echo ========================================
echo [SUCCESS] 🎉 Setup completed successfully!
echo ========================================
echo.
echo ✅ All tests passed! Your system is ready.
echo.
echo 🚀 To start using Video Tool Pro:
echo    1. Make sure this window shows "(venv)" at the prompt
echo    2. Run: python video_tool_app_themed.py
echo    3. Or test themes: python simple_theme_demo.py
echo.
echo 💡 Next time you want to use the app:
echo    1. Open Command Prompt in this folder
echo    2. Run: venv\Scripts\activate
echo    3. Run: python video_tool_app_themed.py
echo.
echo 🎨 Features you can try:
echo    • Download videos from YouTube, TikTok
echo    • Switch between light and dark themes
echo    • Flip, split, and convert videos
echo    • Process multiple videos at once
echo.
echo 📖 For help, check these files:
echo    • START_HERE.md - Quick guide
echo    • WINDOWS_SETUP.md - Windows-specific help
echo    • SETUP_GUIDE.md - Detailed instructions
echo.

REM Final check and user prompt
echo Press any key to start the theme demo, or Ctrl+C to exit...
pause >nul

echo.
echo [INFO] Starting theme demo...
python simple_theme_demo.py
if %errorlevel% neq 0 (
    echo [INFO] Demo couldn't start automatically.
    echo Run: python simple_theme_demo.py
)

echo.
echo 🎉 Setup complete! Enjoy Video Tool Pro! 🎬✨
pause
