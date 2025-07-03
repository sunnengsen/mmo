# 🚀 Video Tool Pro - Complete Setup Guide

This guide will help you clone and run the Video Tool Pro project on any computer.

## 📋 Prerequisites

### Required Software
- **Python 3.8+** (Recommended: Python 3.9 or higher)
- **Git** (for cloning the repository)
- **FFmpeg** (for video processing)

### Operating System Support
- ✅ **macOS** (10.14+)
- ✅ **Windows** (10/11)
- ✅ **Linux** (Ubuntu 18.04+, Debian 10+)

---

## 🔧 Step-by-Step Installation

> **🪟 Windows Users:** For Windows-specific instructions, see [`WINDOWS_SETUP.md`](WINDOWS_SETUP.md) or [`WINDOWS_QUICK_REF.md`](WINDOWS_QUICK_REF.md)

### Step 1: Install Python

#### macOS:
```bash
# Using Homebrew (recommended)
brew install python3

# Or download from https://www.python.org/downloads/
```

#### Windows:
```cmd
# Download from https://www.python.org/downloads/
# ⚠️ IMPORTANT: Check "Add Python to PATH" during installation!

# Verify installation:
python --version
# Should show Python 3.8+
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### Step 2: Install FFmpeg

#### macOS:
```bash
# Using Homebrew
brew install ffmpeg
```

#### Windows:
```cmd
# Option 1: Using Chocolatey (Recommended)
choco install ffmpeg

# Option 2: Using winget (Windows 10/11)  
winget install ffmpeg

# Option 3: Manual installation
# 1. Download from https://ffmpeg.org/download.html
# 2. Extract to C:\ffmpeg
# 3. Add C:\ffmpeg\bin to your PATH environment variable

# Verify installation:
ffmpeg -version
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt install ffmpeg
```

### Step 3: Verify Installations

```bash
# Check Python version
python3 --version
# Should show: Python 3.8.x or higher

# Check FFmpeg
ffmpeg -version
# Should show FFmpeg version information

# Check pip
pip3 --version
# Should show pip version
```

---

## 📦 Project Setup

### Step 1: Clone the Repository

```bash
# Clone the project
git clone <your-repository-url>
cd script_mmo

# Or if you have the project as a zip file:
# 1. Extract the zip file
# 2. Navigate to the extracted folder
cd script_mmo
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Your terminal should now show (venv) at the beginning
```

### Step 3: Install Python Dependencies

```bash
# Make sure virtual environment is activated
pip install -r requirements.txt

# If you get errors, try upgrading pip first:
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Install yt-dlp (YouTube Downloader)

```bash
# Install yt-dlp for video downloading
pip install yt-dlp

# Or using system package manager:
# macOS: brew install yt-dlp
# Ubuntu: sudo apt install yt-dlp
```

---

## 🎮 Running the Application

### Option 1: Run Main Application
```bash
# Make sure virtual environment is activated
python video_tool_app.py
```

### Option 2: Run with Theme Switching
```bash
# Run the enhanced version with dark/light mode
python video_tool_app_themed.py
```

### Option 3: Test Theme Switching
```bash
# Test the theme switching feature
python simple_theme_demo.py
```

---

## 🧪 Testing the Setup

### Test 1: Basic Functionality
```bash
# Test if all modules load correctly
python -c "import PyQt6; print('PyQt6: OK')"
python -c "import ui_styles_new; print('UI Styles: OK')"
python -c "import video_operations; print('Video Operations: OK')"
```

### Test 2: Theme Switching
```bash
# Test theme switching without GUI
python test_theme.py
```

### Test 3: FFmpeg Integration
```bash
# Test if FFmpeg is accessible
ffmpeg -version
yt-dlp --version
```

---

## 📁 Project Structure

```
script_mmo/
├── 📄 README.md                    # Main documentation
├── 📄 requirements.txt             # Python dependencies
├── 📄 video_tool_app.py           # Main application (original)
├── 📄 video_tool_app_themed.py    # Enhanced app with themes
├── 📄 video_operations.py         # Video processing logic
├── 📄 ui_styles.py                # Original UI styles
├── 📄 ui_styles_new.py            # Enhanced UI with themes
├── 📄 worker_thread.py            # Background processing
├── 📄 simple_theme_demo.py        # Theme switching demo
├── 📄 test_theme.py               # Theme testing
├── 📄 integration_guide.py        # Integration examples
├── 📄 THEME_SWITCHING_README.md   # Theme feature docs
└── 📁 venv/                       # Virtual environment
```

---

## 🚨 Troubleshooting

### Common Issues and Solutions

#### Issue 1: "ModuleNotFoundError: No module named 'PyQt6'"
```bash
# Solution: Install PyQt6
pip install PyQt6
```

#### Issue 2: "FFmpeg not found"
```bash
# Solution: Install FFmpeg and add to PATH
# macOS: brew install ffmpeg
# Windows: Download from ffmpeg.org and add to PATH
# Linux: sudo apt install ffmpeg
```

#### Issue 3: "Permission denied" on macOS
```bash
# Solution: Install packages with user flag
pip install --user -r requirements.txt
```

#### Issue 4: Application doesn't start
```bash
# Check if virtual environment is activated
# Look for (venv) at the beginning of your terminal prompt

# If not activated:
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

#### Issue 5: "Qt platform plugin could not be initialized"
```bash
# Solution: Install additional Qt dependencies
pip install PyQt6-Qt6
```

---

## 🎨 Features Available

### Standard Features
- ✅ Video downloading (YouTube, TikTok, etc.)
- ✅ Video flipping (horizontal/vertical)
- ✅ Video splitting
- ✅ Batch processing
- ✅ Progress tracking
- ✅ Activity logging

### Enhanced Features (Themed Version)
- ✅ Light/Dark theme switching
- ✅ Modern UI design
- ✅ Responsive interface
- ✅ Better visual feedback
- ✅ Enhanced button styles

---

## 🔄 Updating the Project

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Update yt-dlp (important for video downloading)
pip install --upgrade yt-dlp
```

---

## 🛠️ Development Setup

If you want to modify the project:

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python test_theme.py
python test_responsive.py

# Run different versions
python video_tool_app.py          # Original
python video_tool_app_themed.py   # With themes
python simple_theme_demo.py       # Theme demo
```

---

## 📞 Support

### Check Your Setup
```bash
# Run this comprehensive check
python -c "
import sys
print(f'Python: {sys.version}')
try:
    import PyQt6
    print('PyQt6: ✅ OK')
except ImportError:
    print('PyQt6: ❌ Missing')
try:
    import ui_styles_new
    print('UI Styles: ✅ OK')
except ImportError:
    print('UI Styles: ❌ Missing')
import subprocess
try:
    subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    print('FFmpeg: ✅ OK')
except:
    print('FFmpeg: ❌ Missing')
try:
    subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
    print('yt-dlp: ✅ OK')
except:
    print('yt-dlp: ❌ Missing')
"
```

### Quick Start Commands
```bash
# Complete setup in one go (after cloning)
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install yt-dlp
python simple_theme_demo.py  # Test run
```

---

## 🎯 Next Steps

1. **Run the demo**: `python simple_theme_demo.py`
2. **Test video download**: Use the main app to download a video
3. **Try theme switching**: Click the theme button in the app
4. **Explore features**: Try video flipping, splitting, and conversion
5. **Check logs**: Monitor the activity log for process information

---

**🎉 You're all set! The Video Tool Pro should now be running on your system.**

For theme switching features, see `THEME_SWITCHING_README.md` for detailed documentation.
