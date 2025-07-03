#!/usr/bin/env python3
"""
Test script to diagnose download issues
"""
import subprocess
import shutil
import sys
import os

def test_download_functionality():
    """Test if download functionality works"""
    print("🔍 Testing Video Download Functionality")
    print("=" * 50)
    
    # Test 1: Check if yt-dlp is available
    print("\n1. Checking yt-dlp availability...")
    ytdlp_path = shutil.which("yt-dlp")
    if ytdlp_path:
        print(f"✅ yt-dlp found at: {ytdlp_path}")
        try:
            result = subprocess.run([ytdlp_path, "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ yt-dlp version: {result.stdout.strip()}")
            else:
                print(f"❌ yt-dlp version check failed: {result.stderr}")
        except Exception as e:
            print(f"❌ Error running yt-dlp: {e}")
    else:
        print("❌ yt-dlp not found in PATH")
    
    # Test 2: Check if ffmpeg is available
    print("\n2. Checking FFmpeg availability...")
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        print(f"✅ FFmpeg found at: {ffmpeg_path}")
        try:
            result = subprocess.run([ffmpeg_path, "-version"], capture_output=True, text=True)
            if result.returncode == 0:
                # Just show first line of version info
                version_line = result.stdout.split('\n')[0]
                print(f"✅ FFmpeg version: {version_line}")
            else:
                print(f"❌ FFmpeg version check failed: {result.stderr}")
        except Exception as e:
            print(f"❌ Error running FFmpeg: {e}")
    else:
        print("❌ FFmpeg not found in PATH")
    
    # Test 3: Check Python packages
    print("\n3. Checking Python packages...")
    try:
        import PyQt6
        print("✅ PyQt6 imported successfully")
    except ImportError as e:
        print(f"❌ PyQt6 import failed: {e}")
    
    try:
        import ui_styles
        print("✅ ui_styles imported successfully")
    except ImportError as e:
        print(f"❌ ui_styles import failed: {e}")
    
    try:
        import video_operations
        print("✅ video_operations imported successfully")
    except ImportError as e:
        print(f"❌ video_operations import failed: {e}")
    
    # Test 4: Test actual download command
    print("\n4. Testing download command (dry run)...")
    if ytdlp_path:
        try:
            # Use a simple test URL and simulate download
            test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll for testing
            cmd = [ytdlp_path, "--simulate", "--get-title", test_url]
            print(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"✅ Download test successful: {result.stdout.strip()}")
            else:
                print(f"❌ Download test failed: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("❌ Download test timed out (network issue?)")
        except Exception as e:
            print(f"❌ Download test error: {e}")
    else:
        print("❌ Cannot test download - yt-dlp not found")
    
    print("\n" + "=" * 50)
    print("🎯 Diagnosis Summary:")
    print("=" * 50)
    
    if not ytdlp_path:
        print("❌ ISSUE: yt-dlp is not installed or not in PATH")
        print("   Fix: Run 'pip install yt-dlp' or check PATH")
    
    if not ffmpeg_path:
        print("❌ ISSUE: FFmpeg is not installed or not in PATH")
        print("   Fix: Install FFmpeg and add to PATH")
    
    if ytdlp_path and ffmpeg_path:
        print("✅ All required tools are available")
        print("   If downloads still fail, check network connection")
        print("   or try a different video URL")

if __name__ == "__main__":
    test_download_functionality()
