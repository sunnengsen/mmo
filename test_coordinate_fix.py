#!/usr/bin/env python3
"""
Test the fixed watermark removal coordinates
"""
import subprocess
import sys
import os

def test_fixed_removal():
    """Test watermark removal with the coordinate fixes"""
    
    video_path = "/Users/sunnengsen/Desktop/part_000.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        return False
    
    # Test the original problematic coordinates with our fixes
    print("🧪 Testing fixed watermark removal...")
    
    # Original coordinates that caused the error
    orig_x, orig_y, orig_w, orig_h = 0, 11, 242, 110
    
    # Apply the same coordinate validation as in worker_thread.py
    video_width, video_height = 1280, 720
    
    # Add padding like in worker_thread.py
    padding = 5
    x = max(0, orig_x - padding)
    y = max(0, orig_y - padding)
    w = orig_w + (2 * padding)
    h = orig_h + (2 * padding)
    
    # Apply coordinate validation
    x = max(1, min(x, video_width - 2))
    y = max(1, min(y, video_height - 2))
    
    max_w = video_width - x - 1
    max_h = video_height - y - 1
    w = min(w, max_w)
    h = min(h, max_h)
    
    print(f"Original coordinates: x={orig_x}, y={orig_y}, w={orig_w}, h={orig_h}")
    print(f"After padding: x={orig_x-padding}, y={orig_y-padding}, w={orig_w+2*padding}, h={orig_h+2*padding}")
    print(f"After validation: x={x}, y={y}, w={w}, h={h}")
    
    if w < 2 or h < 2:
        print(f"❌ Logo area too small: {w}x{h}")
        return False
    
    # Test delogo method (the one that was failing)
    output_path = "test_fixed_removal.mp4"
    cmd = [
        "/opt/homebrew/bin/ffmpeg", "-i", video_path,
        "-vf", f"delogo=x={x}:y={y}:w={w}:h={h}:show=0",
        "-t", "5",  # Only process 5 seconds for testing
        "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-c:a", "copy",
        "-y", output_path
    ]
    
    print(f"\n🚀 Running command:")
    print(f"ffmpeg -i {video_path} -vf delogo=x={x}:y={y}:w={w}:h={h}:show=0 -t 5 -c:v libx264 -crf 23 -preset medium -c:a copy -y {output_path}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ SUCCESS! Watermark removal completed")
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ Output file created: {output_path} ({file_size:,} bytes)")
            
            # Clean up test file
            os.remove(output_path)
            print("✅ Test file cleaned up")
            return True
        else:
            print("❌ Output file was not created")
            return False
    else:
        print("❌ FAILED!")
        print(f"Error: {result.stderr}")
        return False

if __name__ == "__main__":
    success = test_fixed_removal()
    if success:
        print("\n🎉 The coordinate fix is working! Watermark removal should now work in the main app.")
    else:
        print("\n❌ The fix didn't work. Further investigation needed.")
