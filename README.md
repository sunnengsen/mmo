# Video Tool Pro

A professional video processing application built with PyQt6 that provides an easy-to-use interface for downloading, flipping, splitting, and converting videos.

## Features

- **Video Download**: Download videos from YouTube, TikTok, and other platforms using yt-dlp
- **Video Flipping**: Flip videos horizontally, vertically, or both
- **Batch Processing**: Process multiple videos in a folder at once
- **Video Splitting**: Split long videos into smaller segments
- **TikTok/Reel Conversion**: Convert videos to vertical format for social media
- **Progress Tracking**: Real-time progress monitoring and logging

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
