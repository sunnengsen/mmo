# 👋 **Just Got This Project? Start Here!**

## 🚀 **Super Quick Setup (2 minutes)**

1. **Open terminal in this folder**
2. **Run setup:**
   - **Mac/Linux:** `./setup.sh`
   - **Windows:** `setup.bat`
3. **Start app:** `python video_tool_app_themed.py`
4. **Done!** 🎉

---

## 📱 **What This App Does**

- ✅ **Download videos** from YouTube, TikTok, etc.
- ✅ **Flip videos** horizontally/vertically  
- ✅ **Split long videos** into smaller parts
- ✅ **Convert for social media** (TikTok/Reels format)
- ✅ **Switch themes** between light and dark mode
- ✅ **Process multiple videos** at once

---

## 🎯 **First Time Setup**

### **If Automated Setup Doesn't Work:**
```bash
# Manual setup (copy-paste these commands)
python -m venv venv
source venv/bin/activate    # Mac/Linux
# OR
venv\Scripts\activate       # Windows

pip install -r requirements.txt
pip install yt-dlp
python video_tool_app_themed.py
```

### **Need FFmpeg? (For video processing)**
- **Mac:** `brew install ffmpeg`
- **Windows:** Download from [ffmpeg.org](https://ffmpeg.org)
- **Linux:** `sudo apt install ffmpeg`

---

## 🧪 **Test If It's Working**

```bash
# Quick test
python check_system.py

# Try the theme demo
python simple_theme_demo.py
```

---

## 🎮 **How to Use**

1. **Download a video:**
   - Paste YouTube/TikTok URL
   - Click "Download Video"

2. **Switch themes:**
   - Click the theme button (🌙/☀️)
   - Watch everything change color instantly!

3. **Process videos:**
   - Select a video file
   - Choose flip, split, or convert
   - Watch the progress bar

---

## 📁 **Important Files**

- **`video_tool_app_themed.py`** - Main app (with themes)
- **`simple_theme_demo.py`** - Quick theme test
- **`check_system.py`** - Verify everything works
- **`NEW_COMPUTER_SETUP.md`** - Step-by-step checklist
- **`SETUP_GUIDE.md`** - Detailed instructions if you need help

---

## ❓ **Having Issues?**

### **App won't start?**
- Make sure Python 3.8+ is installed
- Check virtual environment is active (should see `(venv)` in terminal)

### **Want more help?**
- Check `NEW_COMPUTER_SETUP.md` for checklist
- Read `SETUP_GUIDE.md` for detailed instructions

---

## 🎉 **You're Ready!**

**Run this to start:** `python video_tool_app_themed.py`

**Click the theme button to see the magic! 🌙 ↔ ☀️**

---

*Made with ❤️ - Enjoy your video tool with awesome theme switching!*
