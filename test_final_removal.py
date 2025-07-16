#!/usr/bin/env python3
"""
Test the full automatic watermark removal process
"""

import sys
import os
sys.path.append('/Users/sunnengsen/Documents/Code/script_mmo')

from logo_detector import LogoDetector

# Mock GUI for testing
class MockGUI:
    def __init__(self):
        self.log_messages = []
    
    def log(self, message):
        self.log_messages.append(message)
        print(f"📋 LOG: {message}")
    
    def update_progress(self, value):
        print(f"⏳ Progress: {value}%")
    
    def finish_operation(self):
        print("✅ Operation finished!")

def test_full_removal():
    print("Testing full automatic watermark removal...")
    
    # Initialize detector
    detector = LogoDetector('/opt/homebrew/bin/ffmpeg')
    
    # Mock GUI
    gui = MockGUI()
    
    # Test video
    video_path = '/Users/sunnengsen/Documents/Code/script_mmo/test_moving_final.mp4'
    output_path = '/Users/sunnengsen/Documents/Code/script_mmo/test_removal_final_improved.mp4'
    
    # Run detection
    print("\n🔍 Running detection...")
    watermarks = detector.detect_logos_with_timeline(video_path)
    
    if not watermarks:
        print("❌ No watermarks detected!")
        return
    
    print(f"✅ Found {len(watermarks)} watermark timelines")
    
    # Show the top watermark
    best_watermark = watermarks[0]
    print(f"\n🎯 Best watermark candidate:")
    print(f"  Text: '{best_watermark.get('text', '')}'")
    print(f"  Type: {best_watermark.get('type', 'unknown')}")
    print(f"  Moving: {best_watermark.get('is_moving', False)}")
    print(f"  Confidence: {best_watermark.get('confidence', 0):.2f}")
    print(f"  Detections: {len(best_watermark.get('detections', []))}")
    
    # Test FFmpeg command generation
    print(f"\n🛠️ Generating FFmpeg command...")
    try:
        ffmpeg_cmd = detector.create_dynamic_removal_command(video_path, best_watermark, method='delogo')
        print(f"FFmpeg command: {' '.join(ffmpeg_cmd)}")
        
        # Test if the command would be valid
        if len(ffmpeg_cmd) > 5:
            print("✅ FFmpeg command generated successfully")
        else:
            print("❌ FFmpeg command seems invalid")
            
    except Exception as e:
        print(f"❌ Error generating FFmpeg command: {e}")
        return
    
    # Now test the actual removal (simulate the video operations)
    print(f"\n🎬 Testing removal process...")
    
    # Show movement analysis
    movement = best_watermark.get('movement_analysis', {})
    print(f"Movement analysis:")
    print(f"  X variance: {movement.get('x_variance', 0):.1f}")
    print(f"  Y variance: {movement.get('y_variance', 0):.1f}")
    print(f"  X range: {movement.get('x_range', 0):.1f}")
    print(f"  Y range: {movement.get('y_range', 0):.1f}")
    
    print(f"\n🎯 This looks like a {'moving' if best_watermark.get('is_moving', False) else 'static'} watermark")
    print(f"Ready for removal with {'dynamic' if best_watermark.get('is_moving', False) else 'static'} approach")

if __name__ == "__main__":
    test_full_removal()
