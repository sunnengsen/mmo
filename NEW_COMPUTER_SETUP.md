# ✅ New Computer Setup Checklist - Video Tool Pro

**Use this checklist when setting up the project on a different computer.**

---

## 🎯 **Before You Start**

□ Make sure you have the project files (cloned or downloaded)  
□ Open terminal/command prompt  
□ Navigate to the project folder: `cd script_mmo`  

---

## 📋 **Step-by-Step Checklist**

### **Step 1: Check What You Have**
□ Run: `python --version` (should be 3.8+)  
□ Run: `pip --version` (should work)  
□ If Python missing → Install from [python.org](https://python.org)  

### **Step 2: Quick Setup (Choose One)**

#### **Option A: Automated Setup (Recommended)**
□ **On Mac/Linux:** Run `./setup.sh`  
□ **On Windows:** Run `setup.bat`  
□ Wait for setup to complete  
□ Skip to Step 4  

#### **Option B: Manual Setup**
□ Run: `python -m venv venv`  
□ **On Mac/Linux:** Run `source venv/bin/activate`  
□ **On Windows:** Run `venv\Scripts\activate`  
□ Run: `pip install -r requirements.txt`  
□ Run: `pip install yt-dlp`  

### **Step 3: Install FFmpeg (Video Processing)**
□ **On Mac:** Run `brew install ffmpeg`  
□ **On Windows:** Download from [ffmpeg.org](https://ffmpeg.org) and add to PATH  
□ **On Linux:** Run `sudo apt install ffmpeg`  

### **Step 4: Test Everything Works**
□ Run: `python check_system.py`  
□ Should see mostly ✅ green checkmarks  
□ If any ❌ red marks, fix those first  

### **Step 5: Start the Application**
□ Make sure virtual environment is active (shows `(venv)` in terminal)  
□ **If not active:** Run activation command from Step 2  
□ Run: `python simple_theme_demo.py` (quick test)  
□ Run: `python video_tool_app_themed.py` (full app)  

---

## 🚀 **Quick Commands Summary**

```bash
# 1. Navigate to project
cd script_mmo

# 2. Setup (choose one)
./setup.sh                    # Mac/Linux automatic
setup.bat                     # Windows automatic
# OR manual setup:
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
pip install -r requirements.txt
pip install yt-dlp

# 3. Test
python check_system.py

# 4. Run
python video_tool_app_themed.py
```

---

## ⚠️ **Common Problems & Quick Fixes**

### **"Python not found"**
□ Install Python from python.org  
□ Make sure "Add to PATH" is checked during install  

### **"pip not found"**
□ Usually comes with Python  
□ Try: `python -m pip --version`  

### **"Permission denied" (Mac/Linux)**
□ Run: `chmod +x setup.sh`  
□ Then: `./setup.sh`  

### **"FFmpeg not found"**
□ **Mac:** `brew install ffmpeg`  
□ **Windows:** Download and add to PATH  
□ **Linux:** `sudo apt install ffmpeg`  

### **"Virtual environment not working"**
□ Delete `venv` folder  
□ Run: `python -m venv venv` again  
□ Activate it properly  

### **"Module not found" errors**
□ Make sure `(venv)` shows in your terminal  
□ If not: activate virtual environment first  
□ Then run the app  

---

## ✅ **Success Indicators**

**You know it's working when:**
□ `python check_system.py` shows mostly green checkmarks  
□ Applications start without errors  
□ Theme button (🌙/☀️) switches colors instantly  
□ No red error messages in terminal  

---

## 🎮 **What You Can Run**

### **Applications to Try:**
□ `python simple_theme_demo.py` - Quick theme demo  
□ `python video_tool_app_themed.py` - Full app with themes  
□ `python video_tool_app.py` - Original app  

### **Test Scripts:**
□ `python test_theme.py` - Test theme switching  
□ `python check_system.py` - Verify installation  

---

## 📞 **Need Help?**

### **Check These Files:**
□ `SETUP_GUIDE.md` - Detailed setup instructions  
□ `QUICK_START.md` - Alternative setup methods  
□ `THEME_SWITCHING_README.md` - Theme features  

### **Common Issues:**
□ **App won't start:** Check virtual environment is active  
□ **Theme not working:** Run `python test_theme.py`  
□ **Video processing fails:** Install FFmpeg  
□ **Download fails:** Check internet connection  

---

## 🎯 **Final Verification**

Run this complete test:
```bash
python -c "
print('=== System Check ===')
import sys; print(f'Python: {sys.version_info.major}.{sys.version_info.minor}')
try: import PyQt6; print('PyQt6: ✅')
except: print('PyQt6: ❌')
try: import ui_styles_new; print('Themes: ✅')
except: print('Themes: ❌')
print('=== Ready to go! ===')
"
```

**If you see ✅ for everything, you're ready!**

---

## 🎉 **You're Done!**

**Start using the app:**
1. Run: `python video_tool_app_themed.py`
2. Click the theme button (🌙/☀️) to test themes
3. Try downloading a video or processing existing ones

**Enjoy your Video Tool Pro with theme switching! 🎬✨**
