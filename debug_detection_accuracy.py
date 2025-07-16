#!/usr/bin/env python3
"""
Debug detection accuracy - check if watermark coordinates are correct
"""

import os
import sys
import tempfile
import subprocess
import cv2
import numpy as np

def create_test_video_with_known_watermark():
    """Create a test video with a watermark at known coordinates"""
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
        video_path = tmp.name
    
    # Create video with watermark at EXACT known position
    cmd = [
        'ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=blue:size=1280x720:duration=3',
        '-vf', 
        'drawtext=text="TEST WATERMARK":fontcolor=white:fontsize=48:x=100:y=100:box=1:boxcolor=red@0.3',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', video_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to create test video: {result.stderr}")
        return None
    
    print(f"✅ Created test video with watermark at (100, 100)")
    print(f"   Expected text: 'TEST WATERMARK'")
    print(f"   Expected size: ~300x60 pixels (approx)")
    
    return video_path

def extract_and_analyze_frame(video_path):
    """Extract frame and analyze watermark position visually"""
    print("\n🔍 EXTRACTING AND ANALYZING FRAME")
    
    # Extract frame
    frame_path = video_path.replace('.mp4', '_frame.png')
    cmd = ['ffmpeg', '-y', '-i', video_path, '-ss', '1', '-vframes', '1', frame_path]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to extract frame: {result.stderr}")
        return None
    
    # Load and analyze frame
    frame = cv2.imread(frame_path)
    if frame is None:
        print("Failed to load frame")
        return None
    
    h, w = frame.shape[:2]
    print(f"Frame size: {w}x{h}")
    
    # Look for the watermark area manually (red box background)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Find red regions (the box background)
    red_lower = np.array([0, 50, 50])
    red_upper = np.array([10, 255, 255])
    red_mask1 = cv2.inRange(hsv, red_lower, red_upper)
    
    red_lower = np.array([170, 50, 50])
    red_upper = np.array([180, 255, 255])
    red_mask2 = cv2.inRange(hsv, red_lower, red_upper)
    
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)
    
    # Find contours
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w_box, h_box = cv2.boundingRect(largest_contour)
        print(f"✅ Found red box at: ({x}, {y}) {w_box}x{h_box}")
        
        # This should be our watermark area
        return frame_path, (x, y, w_box, h_box)
    else:
        print("❌ Could not find red box in frame")
        return frame_path, None

def test_detection_accuracy(video_path, expected_area=None):
    """Test how accurate our detection is"""
    print("\n🎯 TESTING DETECTION ACCURACY")
    
    from logo_detector import detect_logos_automatically
    
    detected_logos = detect_logos_automatically(video_path, '/opt/homebrew/bin/ffmpeg')
    
    if not detected_logos:
        print("❌ No watermarks detected")
        return False
    
    print(f"✅ Detected {len(detected_logos)} watermarks:")
    
    for i, logo in enumerate(detected_logos):
        text = logo.get('text', 'N/A')
        x, y, w, h = logo['x'], logo['y'], logo['width'], logo['height']
        conf = logo.get('confidence', 0)
        
        print(f"   {i+1}. Text: '{text}'")
        print(f"      Position: ({x}, {y}) {w}x{h}")
        print(f"      Confidence: {conf:.3f}")
        print(f"      Type: {logo.get('type', 'unknown')}")
        
        # Compare with expected area if available
        if expected_area:
            exp_x, exp_y, exp_w, exp_h = expected_area
            
            # Calculate overlap
            overlap_x = max(0, min(x + w, exp_x + exp_w) - max(x, exp_x))
            overlap_y = max(0, min(y + h, exp_y + exp_h) - max(y, exp_y))
            overlap_area = overlap_x * overlap_y
            
            detected_area = w * h
            expected_area_size = exp_w * exp_h
            
            overlap_ratio = overlap_area / max(detected_area, expected_area_size)
            
            print(f"      Expected: ({exp_x}, {exp_y}) {exp_w}x{exp_h}")
            print(f"      Overlap ratio: {overlap_ratio:.3f}")
            
            if overlap_ratio > 0.5:
                print(f"      ✅ Good detection accuracy")
            elif overlap_ratio > 0.2:
                print(f"      ⚠️  Partial detection accuracy")
            else:
                print(f"      ❌ Poor detection accuracy")
        
        print()
    
    return True

def test_manual_removal(video_path, coordinates):
    """Test removal with manual coordinates"""
    print(f"\n🛠️  TESTING MANUAL REMOVAL")
    
    if not coordinates:
        print("❌ No coordinates provided")
        return False
    
    x, y, w, h = coordinates
    output_path = video_path.replace('.mp4', '_manual_removed.mp4')
    
    print(f"🎯 Manual removal at: ({x}, {y}) {w}x{h}")
    
    # Test different methods
    methods = [
        ("delogo", f"delogo=x={x}:y={y}:w={w}:h={h}:show=0"),
        ("blur", f"[0:v]crop={w}:{h}:{x}:{y},gblur=sigma=20[blurred];[0:v][blurred]overlay={x}:{y}[out]"),
        ("blackout", f"drawbox=x={x}:y={y}:w={w}:h={h}:color=black:t=fill")
    ]
    
    for method_name, filter_cmd in methods:
        output = output_path.replace('.mp4', f'_{method_name}.mp4')
        
        print(f"   Testing {method_name}...")
        
        if "[" in filter_cmd:
            # Complex filter
            cmd = [
                'ffmpeg', '-y', '-i', video_path,
                '-filter_complex', filter_cmd,
                '-map', '[out]', '-map', '0:a?',
                '-c:v', 'libx264', '-crf', '23', '-preset', 'fast',
                output
            ]
        else:
            # Simple filter
            cmd = [
                'ffmpeg', '-y', '-i', video_path,
                '-vf', filter_cmd,
                '-c:v', 'libx264', '-crf', '23', '-preset', 'fast',
                output
            ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(output):
            size = os.path.getsize(output)
            print(f"   ✅ {method_name}: Success ({size} bytes)")
            os.remove(output)
        else:
            print(f"   ❌ {method_name}: Failed")
            if result.stderr:
                print(f"      Error: {result.stderr[:100]}...")
    
    return True

def main():
    print("🔍 WATERMARK DETECTION ACCURACY TEST")
    print("=" * 60)
    
    # Create test video with known watermark position
    video_path = create_test_video_with_known_watermark()
    if not video_path:
        return
    
    try:
        # Extract frame and find actual watermark position
        frame_path, actual_coords = extract_and_analyze_frame(video_path)
        
        # Test our detection accuracy
        test_detection_accuracy(video_path, actual_coords)
        
        # Test manual removal with correct coordinates
        if actual_coords:
            test_manual_removal(video_path, actual_coords)
        
        print("\n📊 ANALYSIS SUMMARY:")
        if actual_coords:
            print(f"   Actual watermark area: {actual_coords}")
            print(f"   Detection should cover this area for effective removal")
            print(f"   If detection area is too small, watermark will remain visible")
        else:
            print(f"   Could not determine actual watermark area")
        
        print(f"\n💡 RECOMMENDATIONS:")
        print(f"   1. Ensure detection covers the full watermark area")
        print(f"   2. Add padding around detected areas")
        print(f"   3. Use stronger removal methods for text watermarks")
        print(f"   4. Consider multiple passes for complex watermarks")
        
    finally:
        # Clean up
        if os.path.exists(video_path):
            os.remove(video_path)
        
        frame_path = video_path.replace('.mp4', '_frame.png')
        if os.path.exists(frame_path):
            os.remove(frame_path)
        
        print(f"\n🧹 Cleaned up test files")

if __name__ == "__main__":
    main()
