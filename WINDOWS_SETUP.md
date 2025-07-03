# 🪟 Windows Setup Guide - Video Tool Pro

**Complete setup instructions specifically for Windows users.**

---

## 🎯 **Quick Setup for Windows**

### **Option 1: Automated Setup (Recommended)**
```cmd
# 1. Open Command Prompt or PowerShell in the project folder
# 2. Run the Windows setup script
setup.bat

# 3. Start the app
venv\Scripts\activate
python video_tool_app_themed.py
```

### **Option 2: Manual Setup**
```cmd
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pip install yt-dlp

# 4. Run the app
python video_tool_app_themed.py
```

---

## 📋 **Prerequisites for Windows**

### **Required Software**

#### **1. Python 3.8+**
```cmd
# Download from: https://www.python.org/downloads/
# ⚠️ IMPORTANT: Check "Add Python to PATH" during installation!
```

#### **2. FFmpeg (for video processing)**
**Option A: Using Chocolatey (Recommended)**
```cmd
# Install Chocolatey first: https://chocolatey.org/install
# Then install FFmpeg:
choco install ffmpeg
```

**Option B: Manual Installation**
1. Download FFmpeg from: https://ffmpeg.org/download.html#build-windows
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your PATH environment variable

**Option C: Using winget (Windows 10/11)**
```cmd
winget install ffmpeg
```

---

## 🔧 **Step-by-Step Windows Setup**

### **Step 1: Verify Python Installation**
```cmd
# Open Command Prompt (cmd) or PowerShell
python --version
# Should show: Python 3.8.x or higher

# If "python" doesn't work, try:
python3 --version
py --version
```

### **Step 2: Navigate to Project Folder**
```cmd
# Using File Explorer:
# 1. Right-click in the project folder
# 2. Select "Open in Terminal" or "Open PowerShell window here"

# Or using Command Prompt:
cd C:\path\to\your\script_mmo
# Replace with your actual path
```

### **Step 3: Run Windows Setup Script**
```cmd
# Make sure you're in the project folder, then:
setup.bat
```

**The script will:**
- ✅ Check if Python is installed
- ✅ Check if pip is working
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Test the installation
- ✅ Show you next steps

### **Step 4: Start the Application**
```cmd
# Activate virtual environment
venv\Scripts\activate

# You should see (venv) at the beginning of your prompt

# Run the themed application
python video_tool_app_themed.py
```

---

## 🧪 **Testing Your Setup**

### **Test 1: System Check**
```cmd
python check_system.py
```
**Should show mostly ✅ green checkmarks**

### **Test 2: Quick Theme Demo**
```cmd
venv\Scripts\activate
python simple_theme_demo.py
```
**Should open a window with a working theme button**

### **Test 3: Full Application**
```cmd
venv\Scripts\activate
python video_tool_app_themed.py
```
**Should open the complete application**

---

## 🚨 **Windows-Specific Troubleshooting**

### **Issue 1: "Python is not recognized"**
**Cause:** Python not added to PATH during installation

**Solutions:**
```cmd
# Option A: Reinstall Python
# 1. Download from python.org
# 2. During installation, CHECK "Add Python to PATH"

# Option B: Use Python Launcher
py --version
py -m pip --version

# Option C: Add Python to PATH manually
# Add these to your PATH environment variable:
# C:\Users\YourName\AppData\Local\Programs\Python\Python3x\
# C:\Users\YourName\AppData\Local\Programs\Python\Python3x\Scripts\
```

### **Issue 2: "pip is not recognized"**
**Solutions:**
```cmd
# Use Python module syntax
python -m pip --version
python -m pip install -r requirements.txt

# Or reinstall Python with pip
```

### **Issue 3: "FFmpeg not found"**
**Solutions:**
```cmd
# Option A: Install with Chocolatey
choco install ffmpeg

# Option B: Install with winget
winget install ffmpeg

# Option C: Manual installation
# 1. Download from https://ffmpeg.org/download.html
# 2. Extract to C:\ffmpeg
# 3. Add C:\ffmpeg\bin to PATH
```

### **Issue 4: "Virtual environment not working"**
**Solutions:**
```cmd
# Delete existing venv folder
rmdir /s venv

# Create new virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### **Issue 5: "Access is denied" errors**
**Solutions:**
```cmd
# Run Command Prompt as Administrator
# Right-click Command Prompt → "Run as administrator"

# Or use --user flag
pip install --user -r requirements.txt
```

### **Issue 6: PowerShell execution policy**
**If you get execution policy errors:**
```powershell
# In PowerShell, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again:
venv\Scripts\Activate.ps1
```

---

## 🎮 **Windows-Optimized Commands**

### **Always Use These Commands on Windows:**
```cmd
# Activate virtual environment
venv\Scripts\activate

# Deactivate virtual environment
deactivate

# Install packages
pip install package-name

# Run applications
python video_tool_app_themed.py
python simple_theme_demo.py
python check_system.py
```

### **Useful Windows Shortcuts:**
```cmd
# Open Command Prompt in current folder
# Shift + Right-click in folder → "Open PowerShell window here"

# Or type in address bar:
cmd

# Check if virtual environment is active
# Look for (venv) at beginning of prompt
```

---

## 📁 **Windows File Paths**

### **Project Structure:**
```
C:\Users\YourName\Documents\script_mmo\
├── setup.bat                    ← Windows setup script
├── venv\                        ← Virtual environment
│   └── Scripts\
│       └── activate.bat         ← Activation script
├── video_tool_app_themed.py     ← Main application
├── simple_theme_demo.py         ← Theme demo
├── requirements.txt             ← Dependencies
└── check_system.py             ← System check
```

---

## 🎯 **Quick Start Summary for Windows**

1. **Download/clone project** to your computer
2. **Open Command Prompt** in the project folder
3. **Run:** `setup.bat`
4. **Activate environment:** `venv\Scripts\activate`
5. **Start app:** `python video_tool_app_themed.py`
6. **Test themes:** Click the theme button (🌙/☀️)

---

## 🆘 **Need More Help?**

### **Windows-Specific Resources:**
- **Microsoft Python Guide:** https://docs.microsoft.com/en-us/windows/python/
- **Windows PATH Guide:** https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/
- **Command Prompt Basics:** https://www.digitalcitizen.life/command-prompt-how-use-basic-commands/

### **Quick Verification:**
```cmd
# Run this one-liner to check everything:
python -c "import sys; print(f'Python: {sys.version}'); import PyQt6; print('PyQt6: OK'); print('Ready for Video Tool Pro!')"
```

---

## 🎉 **Success! You're Ready**

**When setup is complete, you should have:**
- ✅ Python working in Command Prompt
- ✅ Virtual environment created and activated
- ✅ All dependencies installed
- ✅ FFmpeg ready for video processing
- ✅ Beautiful theme-switching video application!

**Start using:** `python video_tool_app_themed.py`

**Enjoy your Video Tool Pro on Windows! 🎬✨**
