#!/usr/bin/env python3
"""
Test with drawbox method
"""

import sys
import os
sys.path.append('/Users/sunnengsen/Documents/Code/script_mmo')

from logo_detector import LogoDetector

def test_drawbox_removal():
    print("Testing drawbox removal method...")
    
    # Initialize detector
    detector = LogoDetector('/opt/homebrew/bin/ffmpeg')
    
    # Test video
    video_path = '/Users/sunnengsen/Documents/Code/script_mmo/test_moving_final.mp4'
    
    # Run detection
    print("\n🔍 Running detection...")
    watermarks = detector.detect_logos_with_timeline(video_path)
    
    if not watermarks:
        print("❌ No watermarks detected!")
        return
    
    # Show the top watermark
    best_watermark = watermarks[0]
    print(f"\n🎯 Best watermark candidate:")
    print(f"  Text: '{best_watermark.get('text', '')}'")
    print(f"  Type: {best_watermark.get('type', 'unknown')}")
    print(f"  Moving: {best_watermark.get('is_moving', False)}")
    print(f"  Confidence: {best_watermark.get('confidence', 0):.2f}")
    print(f"  Detections: {len(best_watermark.get('detections', []))}")
    
    # Test FFmpeg command generation with drawbox method
    print(f"\n🛠️ Generating FFmpeg command with drawbox method...")
    try:
        ffmpeg_cmd = detector.create_dynamic_removal_command(video_path, best_watermark, method='drawbox')
        print(f"FFmpeg command: {' '.join(ffmpeg_cmd)}")
        
        # Test the command
        print(f"\n🎬 Executing removal command...")
        import subprocess
        result = subprocess.run(ffmpeg_cmd + ['-t', '10', 'test_moving_watermark_removed_drawbox.mp4', '-y'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Moving watermark removal completed successfully!")
            print("🎉 Output: test_moving_watermark_removed_drawbox.mp4")
        else:
            print(f"❌ Removal failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_drawbox_removal()
