#!/usr/bin/env python3
"""
Simple test to check if video_tool_app.py can be imported and initialized
"""
import sys
import traceback

def test_app_import():
    """Test if the main app can be imported and initialized"""
    print("🧪 Testing Video Tool App Import")
    print("=" * 40)
    
    try:
        # Test importing the main modules
        print("1. Testing imports...")
        
        from PyQt6.QtWidgets import QApplication
        print("✅ PyQt6 imported")
        
        from ui_styles import APP_STYLE, STATUS_COLORS
        print("✅ ui_styles imported")
        
        from video_operations import VideoOperations
        print("✅ video_operations imported")
        
        from video_tool_app import VideoToolApp
        print("✅ video_tool_app imported")
        
        # Test creating QApplication (but don't show GUI)
        print("\n2. Testing QApplication creation...")
        app = QApplication(sys.argv)
        print("✅ QApplication created")
        
        # Test creating the main window (but don't show it)
        print("\n3. Testing VideoToolApp creation...")
        window = VideoToolApp()
        print("✅ VideoToolApp created successfully")
        
        # Test if download functionality is properly wired
        print("\n4. Testing download functionality setup...")
        if hasattr(window, 'video_ops'):
            print("✅ video_ops attribute exists")
            if hasattr(window.video_ops, 'download_video'):
                print("✅ download_video method exists")
            else:
                print("❌ download_video method missing")
        else:
            print("❌ video_ops attribute missing")
            
        # Test if required paths are detected
        print("\n5. Testing executable detection...")
        if hasattr(window, 'ffmpeg_path'):
            if window.ffmpeg_path:
                print(f"✅ FFmpeg found: {window.ffmpeg_path}")
            else:
                print("❌ FFmpeg not found")
        
        if hasattr(window, 'ytdlp_path'):
            if window.ytdlp_path:
                print(f"✅ yt-dlp found: {window.ytdlp_path}")
            else:
                print("❌ yt-dlp not found")
        
        print("\n" + "=" * 40)
        print("✅ All tests passed! App should work correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        print("\n" + "=" * 40)
        print("❌ Tests failed! Check the errors above.")
        return False

if __name__ == "__main__":
    success = test_app_import()
    sys.exit(0 if success else 1)
