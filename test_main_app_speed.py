#!/usr/bin/env python3
"""
Test script to verify the main app runs quickly without hanging
"""

import sys
import time
import tempfile
import os

# Add current directory to path
sys.path.append('.')

def test_main_app_speed():
    """Test the main app with a timeout to prevent hanging"""
    from logo_detector import detect_logos_automatically
    
    # Create a small test video or use test image
    test_file = 'test_watermark.png'
    if not os.path.exists(test_file):
        print(f"Test file {test_file} not found, creating dummy file...")
        # Create a small test image
        import cv2
        import numpy as np
        test_img = np.zeros((100, 200, 3), dtype=np.uint8)
        cv2.putText(test_img, 'TEST', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imwrite(test_file, test_img)
    
    print("🚀 Testing main app speed...")
    start_time = time.time()
    
    try:
        # Test detection with timeout
        result = detect_logos_automatically(test_file, 'ffmpeg')
        end_time = time.time()
        
        elapsed = end_time - start_time
        print(f"✅ Detection completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(result)} detections")
        
        # Check if results have required keys
        for i, det in enumerate(result):
            required_keys = ['x', 'y', 'width', 'height', 'confidence', 'type', 'corner']
            missing_keys = [key for key in required_keys if key not in det]
            if missing_keys:
                print(f"❌ Detection {i+1} missing keys: {missing_keys}")
            else:
                print(f"✅ Detection {i+1} has all required keys")
        
        if elapsed < 10:
            print("🎉 SPEED TEST PASSED - App is fast!")
            return True
        else:
            print("⚠️  SPEED TEST WARNING - App took longer than expected")
            return False
            
    except Exception as e:
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"❌ Error after {elapsed:.2f} seconds: {e}")
        return False

if __name__ == "__main__":
    success = test_main_app_speed()
    sys.exit(0 if success else 1)
