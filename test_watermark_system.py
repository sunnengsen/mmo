#!/usr/bin/env python3
"""
Comprehensive test for watermark removal system
Tests both detection and removal with coordinate validation
"""

import os
import sys
import subprocess
from logo_detector import LogoDetector

def test_watermark_removal():
    """Test the complete watermark removal pipeline"""
    
    print("🧪 Testing Watermark Removal System")
    print("=" * 50)
    
    # Test video
    test_video = "test_simple_watermark.mp4"
    
    if not os.path.exists(test_video):
        print(f"❌ Test video {test_video} not found!")
        return False
    
    # 1. Test detection
    print("\n1. Testing watermark detection...")
    detector = LogoDetector("ffmpeg")
    timelines = detector.detect_logos_with_timeline(test_video, sample_interval=2.0)
    
    if not timelines:
        print("❌ No watermarks detected!")
        return False
    
    print(f"✅ Detected {len(timelines)} watermark timelines")
    
    # 2. Test coordinate validation
    print("\n2. Testing coordinate validation...")
    timeline = timelines[0]
    positions = timeline.get('positions', [])
    
    if not positions:
        print("❌ No position data found!")
        return False
    
    best_position = max(positions, key=lambda p: p.get('confidence', 0))
    
    # Get video dimensions
    probe_cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0", 
        "-show_entries", "stream=width,height", "-of", "csv=p=0", test_video
    ]
    probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
    
    if probe_result.returncode != 0:
        print("❌ Failed to get video dimensions!")
        return False
    
    dimensions = probe_result.stdout.strip().split(',')
    video_width, video_height = int(dimensions[0]), int(dimensions[1])
    
    print(f"📺 Video dimensions: {video_width}x{video_height}")
    
    # Validate coordinates
    x, y, w, h = best_position['x'], best_position['y'], best_position['width'], best_position['height']
    print(f"🔍 Original coordinates: x={x}, y={y}, w={w}, h={h}")
    
    # Apply validation
    x = max(0, min(x, video_width - 1))
    y = max(0, min(y, video_height - 1))
    max_w = video_width - x
    max_h = video_height - y
    w = min(w, max_w - 1)
    h = min(h, max_h - 1)
    w = max(w, 2)
    h = max(h, 2)
    
    print(f"✅ Validated coordinates: x={x}, y={y}, w={w}, h={h}")
    print(f"📏 Area extends to: x+w={x+w}, y+h={y+h} (within {video_width}x{video_height})")
    
    # 3. Test FFmpeg removal
    print("\n3. Testing FFmpeg watermark removal...")
    output_file = "test_removal_final.mp4"
    
    # Remove existing output file
    if os.path.exists(output_file):
        os.remove(output_file)
    
    # Run FFmpeg command
    ffmpeg_cmd = [
        "ffmpeg", "-i", test_video,
        "-vf", f"delogo=x={x}:y={y}:w={w}:h={h}",
        "-c:a", "copy",
        output_file, "-y"
    ]
    
    print(f"🎬 Running: {' '.join(ffmpeg_cmd)}")
    
    result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ FFmpeg failed: {result.stderr}")
        return False
    
    if not os.path.exists(output_file):
        print(f"❌ Output file {output_file} was not created!")
        return False
    
    # Check file size
    file_size = os.path.getsize(output_file)
    print(f"✅ Output file created: {output_file} ({file_size} bytes)")
    
    # 4. Test other removal methods
    print("\n4. Testing alternative removal methods...")
    
    # Test blur method
    blur_output = "test_removal_blur.mp4"
    blur_cmd = [
        "ffmpeg", "-i", test_video,
        "-filter_complex", f"[0:v]crop={w}:{h}:{x}:{y},gblur=sigma=15[blurred];[0:v][blurred]overlay={x}:{y}[out]",
        "-map", "[out]", "-map", "0:a?",
        "-c:v", "libx264", "-crf", "23", "-c:a", "copy",
        blur_output, "-y"
    ]
    
    blur_result = subprocess.run(blur_cmd, capture_output=True, text=True)
    
    if blur_result.returncode == 0 and os.path.exists(blur_output):
        print(f"✅ Blur method works: {blur_output}")
    else:
        print(f"⚠️ Blur method failed: {blur_result.stderr}")
    
    print("\n🎉 Watermark removal system test completed!")
    print("=" * 50)
    
    # Summary
    print("\n📊 Test Summary:")
    print(f"✅ Detection: {len(timelines)} watermarks found")
    print(f"✅ Coordinate validation: {x},{y},{w},{h} (validated)")
    print(f"✅ Delogo removal: {output_file} created")
    print(f"{'✅' if os.path.exists(blur_output) else '⚠️'} Blur removal: {'Success' if os.path.exists(blur_output) else 'Failed'}")
    
    return True

if __name__ == "__main__":
    success = test_watermark_removal()
    sys.exit(0 if success else 1)
