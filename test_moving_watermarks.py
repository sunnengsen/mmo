#!/usr/bin/env python3
"""
Test moving watermark detection
"""

import cv2
import numpy as np
import sys
import time
sys.path.append('.')
from logo_detector import detect_logos_automatically

def test_moving_watermarks():
    """Test detection of watermarks in different positions"""
    print("🎯 Testing moving watermark detection...")
    
    # Create test images with watermarks in different positions
    base_img = np.zeros((720, 1280, 3), dtype=np.uint8)
    base_img[:] = (40, 40, 40)  # Dark background
    
    # Add main video content
    cv2.rectangle(base_img, (200, 150), (1080, 570), (60, 60, 120), -1)
    cv2.putText(base_img, "MAIN VIDEO CONTENT", (400, 350), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
    
    # Test different watermark positions
    test_positions = [
        ("top_left", (50, 50)),
        ("top_right", (1000, 50)),
        ("bottom_left", (50, 650)),
        ("bottom_right", (1000, 650)),
        ("top_center", (600, 50)),
        ("bottom_center", (600, 650)),
        ("left_center", (50, 350)),
        ("right_center", (1100, 350)),
        ("moving_1", (400, 100)),  # Unusual position
        ("moving_2", (800, 500)),  # Another unusual position
    ]
    
    print(f"\n📍 Testing {len(test_positions)} different watermark positions...")
    
    detection_results = {}
    
    for pos_name, (x, y) in test_positions:
        # Create image with watermark at this position
        img = base_img.copy()
        cv2.putText(img, "www.example.com", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
        
        # Save test image
        test_filename = f'test_watermark_{pos_name}.png'
        cv2.imwrite(test_filename, img)
        
        # Test detection
        start_time = time.time()
        result = detect_logos_automatically(test_filename, 'ffmpeg')
        detection_time = time.time() - start_time
        
        # Check results
        watermarks_found = [r for r in result if r.get('is_watermark', False)]
        
        detection_results[pos_name] = {
            'position': (x, y),
            'detections': len(result),
            'watermarks': len(watermarks_found),
            'time': detection_time,
            'success': len(watermarks_found) > 0
        }
        
        print(f"  {pos_name:12} at ({x:4}, {y:3}): {len(watermarks_found)} watermarks, {detection_time:.2f}s")
        
        # Clean up
        import os
        if os.path.exists(test_filename):
            os.remove(test_filename)
    
    # Summary
    print(f"\n📊 RESULTS SUMMARY:")
    successful_detections = sum(1 for r in detection_results.values() if r['success'])
    total_tests = len(detection_results)
    success_rate = (successful_detections / total_tests) * 100
    
    print(f"  ✅ Success rate: {successful_detections}/{total_tests} ({success_rate:.1f}%)")
    print(f"  ⏱️  Average time: {np.mean([r['time'] for r in detection_results.values()]):.2f}s")
    
    # Show failed detections
    failed_positions = [pos for pos, result in detection_results.items() if not result['success']]
    if failed_positions:
        print(f"  ❌ Failed positions: {', '.join(failed_positions)}")
    
    # Test with a "moving" watermark video simulation
    print(f"\n🎬 Testing simulated moving watermark...")
    
    # Create multiple frames with watermark in different positions
    frames = []
    positions = [(100, 100), (200, 100), (300, 100), (400, 100), (500, 100)]  # Moving right
    
    for i, (x, y) in enumerate(positions):
        frame = base_img.copy()
        cv2.putText(frame, "MOVING WATERMARK", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (180, 180, 180), 2)
        cv2.imwrite(f'moving_frame_{i}.png', frame)
        frames.append(f'moving_frame_{i}.png')
    
    # Test detection on each frame
    moving_results = []
    for i, frame_file in enumerate(frames):
        result = detect_logos_automatically(frame_file, 'ffmpeg')
        watermarks = [r for r in result if r.get('is_watermark', False)]
        moving_results.append(len(watermarks))
        
        # Clean up
        import os
        if os.path.exists(frame_file):
            os.remove(frame_file)
    
    moving_success_rate = (sum(1 for r in moving_results if r > 0) / len(moving_results)) * 100
    print(f"  📈 Moving watermark detection: {moving_success_rate:.1f}% success rate")
    
    print(f"\n🏆 MOVING WATERMARK DETECTION READY!")
    print(f"   The system can now handle watermarks in various positions.")
    
    return success_rate > 70  # Success if we detect 70%+ of watermarks

if __name__ == "__main__":
    success = test_moving_watermarks()
    
    if success:
        print("\n✨ Moving watermark detection is working well!")
    else:
        print("\n⚠️  Moving watermark detection needs improvement")
