# 🎬 Video Tool Pro - Enhanced with Theme Switching

A professional video processing application with beautiful light/dark theme switching, built with PyQt6.

## ✨ **New Theme Features**
- 🌙 **Dark Mode** - Easy on the eyes
- ☀️ **Light Mode** - Clean and professional  
- 🔄 **Instant Switching** - One-click theme toggle
- 🎨 **Complete UI Update** - All elements change automatically

## 🚀 **Quick Setup for New Users**

### **Just cloned this project? Start here:**

1. **Read first:** [`START_HERE.md`](START_HERE.md) - Quick 2-minute setup
2. **Detailed setup:** [`NEW_COMPUTER_SETUP.md`](NEW_COMPUTER_SETUP.md) - Step-by-step checklist
3. **Need help?** [`SETUP_GUIDE.md`](SETUP_GUIDE.md) - Complete instructions

### **Super Quick Setup:**
```bash
# Automated setup (recommended)
./setup.sh          # Mac/Linux
setup.bat           # Windows

# Start the app
python video_tool_app_themed.py
```

## 📋 **Core Features**

### **Video Processing**
- ✅ **Download** videos from YouTube, TikTok, Instagram, etc.
- ✅ **Flip** videos horizontally, vertically, or both
- ✅ **Split** long videos into smaller segments
- ✅ **Convert** to TikTok/Reel format (vertical)
- ✅ **Batch process** multiple videos at once
- ✅ **Real-time progress** tracking and logging

### **Enhanced UI**
- ✅ **Theme switching** between light and dark modes
- ✅ **Modern design** with rounded corners and gradients
- ✅ **Responsive interface** with instant feedback
- ✅ **Professional styling** for all UI elements
- ✅ **Visual status indicators** with color coding

## Project Structure

```
script_mmo/
├── app.py                 # Main entry point - simplified launcher
├── video_tool_app.py      # Main application window class
├── video_operations.py    # Video processing operations handler
├── worker_thread.py       # Background worker thread for processing
├── ui_styles.py           # UI styling constants and stylesheets
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install FFmpeg:
   - **macOS**: `brew install ffmpeg`
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - **Ubuntu/Debian**: `sudo apt install ffmpeg`

3. Install yt-dlp (if not already installed):
```bash
pip install yt-dlp
```

## Usage

Run the application:
```bash
python app.py
```

## File Organization

### `app.py`
- Simple entry point that launches the main application
- Keeps the main file clean and focused

### `video_tool_app.py`
- Contains the main `VideoToolApp` class
- Handles UI setup, styling, and user interactions
- Manages application state and progress tracking

### `video_operations.py`
- Contains the `VideoOperations` class
- Handles all video processing logic
- Provides methods for download, flip, split, and convert operations

### `worker_thread.py`
- Contains the `WorkerThread` class
- Runs video processing operations in background threads
- Prevents UI freezing during long operations

### `ui_styles.py`
- Contains all UI styling constants
- Defines the application's visual appearance
- Includes color schemes and CSS stylesheets

## Key Features of the Modular Design

1. **Separation of Concerns**: Each file has a specific purpose
2. **Maintainability**: Easy to modify individual components
3. **Reusability**: Components can be used independently
4. **Testing**: Individual modules can be tested separately
5. **Scalability**: Easy to add new features without cluttering

## Dependencies

- **PyQt6**: Modern GUI framework
- **yt-dlp**: Video downloading from various platforms
- **FFmpeg**: Video processing backend (system dependency)

## License

This project is open source and available under the MIT License.
