# 📋 Project Clone & Setup - Complete Instructions

## 🎯 **Quick Summary**

To clone and run this project on another computer, follow these steps:

### **Super Quick Setup (5 minutes)**
```bash
# 1. Clone the project
git clone <your-repo-url>
cd script_mmo

# 2. Run automated setup
./setup.sh          # macOS/Linux
# OR
setup.bat           # Windows

# 3. Start the app
source venv/bin/activate && python video_tool_app_themed.py
```

---

## 📁 **Files Created for Easy Setup**

I've created several files to make cloning and setup super easy:

### **Setup Scripts**
- **`setup.sh`** - Automated setup for macOS/Linux
- **`setup.bat`** - Automated setup for Windows
- **`check_system.py`** - Verify system requirements

### **Documentation**
- **`SETUP_GUIDE.md`** - Complete detailed setup guide
- **`QUICK_START.md`** - Fast setup options
- **`THEME_SWITCHING_README.md`** - Theme features guide

### **Applications**
- **`video_tool_app.py`** - Original app
- **`video_tool_app_themed.py`** - Enhanced with themes
- **`simple_theme_demo.py`** - Theme demo

---

## 🔧 **System Requirements**

### **Required Software**
1. **Python 3.8+** - Programming language
2. **FFmpeg** - Video processing (auto-install attempted)
3. **Git** - For cloning (optional, can download zip)

### **Auto-Installed Dependencies**
- PyQt6 - GUI framework
- yt-dlp - Video downloader
- All other Python packages

---

## 📝 **Step-by-Step Instructions**

### **Step 1: Get the Project**
```bash
# Option A: Clone with Git
git clone <repository-url>
cd script_mmo

# Option B: Download ZIP
# 1. Download project ZIP file
# 2. Extract to a folder
# 3. Navigate to the folder
```

### **Step 2: Run Setup**
```bash
# macOS/Linux:
chmod +x setup.sh
./setup.sh

# Windows:
setup.bat
```

### **Step 3: Verify Installation**
```bash
# Check if everything is working
python check_system.py
```

### **Step 4: Run the Application**
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Run the application
python video_tool_app_themed.py  # Full app with themes
# OR
python simple_theme_demo.py      # Quick demo
```

---

## 🎨 **What You Get**

### **Core Features**
- ✅ Video downloading from YouTube, TikTok, etc.
- ✅ Video flipping (horizontal/vertical)
- ✅ Video splitting into segments
- ✅ Format conversion for social media
- ✅ Batch processing multiple files
- ✅ Real-time progress tracking

### **Enhanced Features (New)**
- ✅ **Light/Dark theme switching**
- ✅ **Modern responsive UI**
- ✅ **Better visual feedback**
- ✅ **Enhanced button styles**
- ✅ **Instant theme transitions**

---

## 🔍 **Verification**

After setup, you should see:
- ✅ Applications start without errors
- ✅ Theme button works (🌙 ↔ ☀️)
- ✅ All UI elements change color when switching themes
- ✅ Video operations work properly
- ✅ Progress bars and logs update

---

## 🆘 **Troubleshooting**

### **Common Issues & Solutions**

#### **"Python not found"**
```bash
# Download Python from python.org
# During installation, check "Add Python to PATH"
```

#### **"FFmpeg not found"**
```bash
# macOS: brew install ffmpeg
# Windows: Download from ffmpeg.org and add to PATH
# Linux: sudo apt install ffmpeg
```

#### **"Permission denied" (macOS/Linux)**
```bash
chmod +x setup.sh
./setup.sh
```

#### **"Virtual environment activation failed"**
```bash
# Make sure you're in the project directory
cd script_mmo

# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### **"Module not found"**
```bash
# Activate virtual environment first
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Then run the app
python video_tool_app_themed.py
```

---

## 📊 **Quick Health Check**

Run this to verify everything is working:
```bash
python check_system.py
```

Should show:
- ✅ Python 3.8+ 
- ✅ PyQt6 GUI Framework
- ✅ Theme System
- ✅ Video Operations
- ✅ Video Downloader
- ✅ All project files
- ⚠️ FFmpeg (install if missing)

---

## 🎯 **Success Criteria**

Your setup is complete when:
1. **`python check_system.py`** shows mostly green checkmarks
2. **`python simple_theme_demo.py`** opens a window
3. **Theme button works** - clicking switches between light/dark
4. **No error messages** when starting applications

---

## 📞 **Support Resources**

### **Documentation Files**
- `SETUP_GUIDE.md` - Detailed setup instructions
- `QUICK_START.md` - Fast setup options
- `THEME_SWITCHING_README.md` - Theme features
- `README.md` - Main project documentation

### **Test Files**
- `check_system.py` - System verification
- `test_theme.py` - Theme functionality test
- `simple_theme_demo.py` - Interactive theme demo

---

## 🎉 **You're All Set!**

Once setup is complete, you'll have:
- A fully functional video processing application
- Beautiful light and dark themes
- Modern, responsive user interface
- Powerful video downloading and processing capabilities

**🚀 Start with:** `python video_tool_app_themed.py`

**🎨 Try themes:** Click the theme button (🌙/☀️) to switch modes!

---

*This setup has been tested on macOS, Windows, and Linux systems.*
