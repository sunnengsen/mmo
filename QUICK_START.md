# 🚀 Quick Start Guide - Video Tool Pro

Choose your setup method based on your situation:

## 📥 **Option 1: First Time Setup (Recommended)**

### For macOS/Linux:
```bash
# 1. Clone or download the project
git clone <repository-url>  # or extract zip file
cd script_mmo

# 2. Run automated setup
chmod +x setup.sh
./setup.sh

# 3. Start the application
source venv/bin/activate
python video_tool_app_themed.py
```

### For Windows:
```cmd
# 1. Clone or download the project
git clone <repository-url>  # or extract zip file
cd script_mmo

# 2. Run automated setup
setup.bat

# 3. Start the application
venv\Scripts\activate
python video_tool_app_themed.py
```

---

## ⚡ **Option 2: Manual Quick Setup**

```bash
# 1. Navigate to project folder
cd script_mmo

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# 4. Install dependencies
pip install -r requirements.txt
pip install yt-dlp

# 5. Run the app
python video_tool_app_themed.py
```

---

## 🧪 **Option 3: Test First (Verify System)**

```bash
# Check if your system is ready
python check_system.py

# If all checks pass, run the app
python simple_theme_demo.py  # Quick demo
```

---

## 🎯 **What You Get**

### Main Applications:
- **`video_tool_app.py`** - Original application
- **`video_tool_app_themed.py`** - Enhanced with dark/light themes
- **`simple_theme_demo.py`** - Theme switching demo

### Key Features:
- ✅ **Video Download** - YouTube, TikTok, etc.
- ✅ **Video Processing** - Flip, split, convert
- ✅ **Theme Switching** - Light/Dark modes
- ✅ **Batch Processing** - Multiple files
- ✅ **Progress Tracking** - Real-time updates

---

## 🔧 **Prerequisites**

### Must Have:
- **Python 3.8+** 
- **FFmpeg** (for video processing)

### Auto-Installed:
- **PyQt6** (GUI framework)
- **yt-dlp** (video downloader)

---

## ⚠️ **Common Issues**

### "Python not found"
```bash
# Install Python from python.org
# Make sure to add to PATH during installation
```

### "FFmpeg not found"
```bash
# macOS: brew install ffmpeg
# Windows: Download from ffmpeg.org
# Linux: sudo apt install ffmpeg
```

### "ModuleNotFoundError"
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Then reinstall
pip install -r requirements.txt
```

---

## 🎮 **Usage Examples**

### Download a Video:
1. Open the app
2. Paste video URL
3. Select download folder
4. Click "Download Video"

### Switch Themes:
1. Click theme button (🌙/☀️)
2. Interface instantly changes
3. All colors update automatically

### Process Videos:
1. Select video file
2. Choose operation (flip, split, convert)
3. Monitor progress in real-time

---

## 📚 **Documentation**

- **`SETUP_GUIDE.md`** - Complete installation guide
- **`THEME_SWITCHING_README.md`** - Theme features documentation
- **`README.md`** - Main project documentation

---

## 🆘 **Getting Help**

### Self-Diagnosis:
```bash
# Check your system
python check_system.py

# Test theme functionality
python test_theme.py

# View detailed logs
# Check the Activity Log in the application
```

### File Issues:
- Missing files? Re-download/clone the project
- Permission errors? Run as administrator (Windows) or use sudo (Linux)
- Path issues? Use absolute paths

---

## 🎉 **Success Indicators**

You'll know it's working when:
- ✅ Applications start without errors
- ✅ Theme switching works instantly
- ✅ Video download/processing completes
- ✅ Progress bars and logs update properly

---

**🚀 Ready to go? Pick your option above and start in 5 minutes!**
