#!/usr/bin/env python3
"""
Simple coordinate debug
"""

import sys
import os
sys.path.append('/Users/sunnengsen/Documents/Code/script_mmo')

from logo_detector import LogoDetector

def simple_debug():
    print("Simple coordinate debug...")
    
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
    print(f"  Detections: {len(best_watermark.get('detections', []))}")
    
    # Show all detections with coordinates
    print(f"\n📍 All detections:")
    for i, det in enumerate(best_watermark.get('detections', [])):
        x, y, w, h = det['x'], det['y'], det['width'], det['height']
        print(f"  {i+1}. '{det.get('text', '')}' at ({x}, {y}) size {w}x{h} t={det.get('timestamp', 0):.1f}s")
        print(f"     Right edge: {x + w} (frame width: 640)")
        print(f"     Bottom edge: {y + h} (frame height: 480)")
        if x + w > 640:
            print(f"     ❌ Exceeds frame width by {x + w - 640} pixels")
        if y + h > 480:
            print(f"     ❌ Exceeds frame height by {y + h - 480} pixels")
    
    # Test FFmpeg command generation
    print(f"\n🛠️ Generating FFmpeg command...")
    try:
        ffmpeg_cmd = detector.create_dynamic_removal_command(video_path, best_watermark, method='delogo')
        print(f"FFmpeg command: {' '.join(ffmpeg_cmd)}")
        
        # Extract the filter part
        vf_index = ffmpeg_cmd.index('-vf')
        if vf_index + 1 < len(ffmpeg_cmd):
            filter_str = ffmpeg_cmd[vf_index + 1]
            print(f"\nFilter string: {filter_str}")
            
            # Parse and validate each delogo filter
            filters = filter_str.split(',')
            for i, filter_part in enumerate(filters):
                print(f"\nFilter {i+1}: {filter_part}")
                if 'delogo=' in filter_part:
                    # Extract coordinates
                    import re
                    match = re.search(r'delogo=x=(\d+):y=(\d+):w=(\d+):h=(\d+)', filter_part)
                    if match:
                        x, y, w, h = map(int, match.groups())
                        print(f"  Coordinates: x={x}, y={y}, w={w}, h={h}")
                        print(f"  Right edge: {x + w} (frame width: 640)")
                        print(f"  Bottom edge: {y + h} (frame height: 480)")
                        if x + w > 640:
                            print(f"  ❌ Still exceeds frame width by {x + w - 640} pixels")
                        if y + h > 480:
                            print(f"  ❌ Still exceeds frame height by {y + h - 480} pixels")
                        else:
                            print(f"  ✅ Coordinates are valid")
                            
    except Exception as e:
        print(f"❌ Error generating FFmpeg command: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simple_debug()
