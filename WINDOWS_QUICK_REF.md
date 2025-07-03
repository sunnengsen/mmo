# 🪟 Windows Quick Reference - Video Tool Pro

## 🚀 **Super Quick Setup**

```cmd
# 1. Open Command Prompt in project folder
# 2. Run setup
setup.bat

# 3. Start the app
venv\Scripts\activate
python video_tool_app_themed.py
```

---

## 📋 **Essential Windows Commands**

### **Virtual Environment**
```cmd
# Create
python -m venv venv

# Activate (you'll see "(venv)" in prompt)
venv\Scripts\activate

# Deactivate
deactivate
```

### **Run Applications**
```cmd
# Always activate first!
venv\Scripts\activate

# Then run any of these:
python video_tool_app_themed.py    # Main app with themes
python simple_theme_demo.py        # Quick theme test
python check_system.py            # Verify setup
```

---

## 🔧 **Windows-Specific Fixes**

### **Python Not Found**
```cmd
# Check if Python is installed
python --version
py --version
python3 --version

# If none work, reinstall Python from python.org
# ⚠️ CHECK "Add Python to PATH" during install!
```

### **FFmpeg Not Found**
```cmd
# Option 1: Chocolatey (easiest)
choco install ffmpeg

# Option 2: winget (Windows 10/11)
winget install ffmpeg

# Option 3: Manual download from ffmpeg.org
```

### **Permission Errors**
```cmd
# Run Command Prompt as Administrator
# Right-click "Command Prompt" → "Run as administrator"
```

### **PowerShell Execution Policy**
```powershell
# If using PowerShell and getting policy errors:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📁 **Windows File Locations**

### **Common Project Locations**
```
C:\Users\YourName\Documents\script_mmo\
C:\Users\YourName\Desktop\script_mmo\
C:\projects\script_mmo\
```

### **Virtual Environment Location**
```
script_mmo\venv\Scripts\activate.bat  ← Activation script
```

---

## 🎯 **Quick Checklist**

- [ ] Python 3.8+ installed with PATH
- [ ] Project folder downloaded/cloned
- [ ] Command Prompt opened in project folder
- [ ] `setup.bat` completed successfully
- [ ] Virtual environment activated (shows `(venv)`)
- [ ] App starts: `python video_tool_app_themed.py`
- [ ] Theme button works (🌙 ↔ ☀️)

---

## 🆘 **Emergency Commands**

### **If Everything Breaks**
```cmd
# Delete and recreate virtual environment
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install yt-dlp
```

### **Quick System Check**
```cmd
python check_system.py
```

### **Test Just Themes**
```cmd
venv\Scripts\activate
python simple_theme_demo.py
```

---

## 🎮 **What You Get**

- **Video Downloader** - YouTube, TikTok, Instagram
- **Video Processor** - Flip, split, convert videos
- **Theme Switching** - Beautiful light/dark modes
- **Batch Processing** - Handle multiple files
- **Progress Tracking** - Real-time status updates

---

## 📞 **Help Files**

- **`WINDOWS_SETUP.md`** - Complete Windows guide
- **`START_HERE.md`** - General quick start
- **`SETUP_GUIDE.md`** - Detailed instructions

---

**🎉 Ready to go? Run `setup.bat` and start creating! 🎬✨**
