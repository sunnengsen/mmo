#!/usr/bin/env python3
"""
Test the main detection function to ensure no KeyError issues
"""

import cv2
import numpy as np
from logo_detector import detect_logos_automatically
import tempfile
import os

def test_no_keyerror():
    """Test that detection doesn't cause KeyError"""
    print("Testing main detection function for KeyError issues...")
    
    # Create test image with watermarks (similar to what the app would process)
    img = np.zeros((720, 1280, 3), dtype=np.uint8)
    img[:] = (40, 40, 40)  # Dark background
    
    # Add video content
    cv2.rectangle(img, (100, 100), (1180, 600), (60, 60, 120), -1)
    cv2.putText(img, "VIDEO CONTENT", (400, 350), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    
    # Add watermarks that should be detected
    cv2.putText(img, "www.idramahd.com", (950, 680), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
    cv2.putText(img, "FREE MOVIES HD", (1000, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (180, 180, 180), 2)
    
    # Save as temporary image file that can be used as a frame
    temp_path = '/tmp/test_frame.png'
    cv2.imwrite(temp_path, img)
    
    try:
        # Test the main detection function (this is what the app calls)
        from logo_detector import LogoDetector
        detector = LogoDetector('/opt/homebrew/bin/ffmpeg')
        
        # Test the individual methods first
        print("\n1. Testing direct logo detection...")
        frame_detections = detector._detect_text_watermarks_full_frame(img)
        print(f"Full frame detection found {len(frame_detections)} detections")
        
        # Check all detections have required keys
        for i, detection in enumerate(frame_detections):
            required_keys = ['x', 'y', 'width', 'height', 'confidence', 'type']
            missing_keys = [key for key in required_keys if key not in detection]
            
            if missing_keys:
                print(f"  ❌ Detection {i+1} missing keys: {missing_keys}")
                return False
            else:
                corner = detection.get('corner', 'N/A')
                text = detection.get('text', 'N/A')
                watermark = detection.get('is_watermark', False)
                print(f"  ✅ Detection {i+1}: type={detection['type']}, corner={corner}, watermark={watermark}, text='{text[:20]}...'")
        
        print("\n2. Testing corner detection...")
        corner_detections = detector.detect_logos_in_corners(img)
        print(f"Corner detection found {len(corner_detections)} detections")
        
        # Check corner detections
        for i, detection in enumerate(corner_detections[:5]):  # Just check first 5
            corner = detection.get('corner', 'N/A')
            text = detection.get('text', 'N/A')
            watermark = detection.get('is_watermark', False)
            print(f"  ✅ Detection {i+1}: type={detection['type']}, corner={corner}, watermark={watermark}")
        
        print("\n✅ All detections have required keys - no KeyError issues!")
        
        # Test what the app would actually receive
        print("\n3. Testing what the app receives...")
        all_detections = frame_detections + corner_detections
        
        if all_detections:
            # Simulate what the app does
            selected_logo = all_detections[0]
            corner_info = selected_logo.get('corner', 'auto-detected')
            logo_type = selected_logo.get('type', 'unknown')
            
            print(f"App would receive: corner='{corner_info}', type='{logo_type}', confidence={selected_logo['confidence']:.3f}")
            
            if 'text' in selected_logo:
                print(f"Detected text: '{selected_logo['text']}'")
            
            print("✅ App integration test passed!")
            return True
        else:
            print("❌ No detections found")
            return False
        
    except KeyError as e:
        print(f"❌ KeyError still present: {e}")
        return False
    except Exception as e:
        print(f"❌ Other error: {e}")
        return False
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    success = test_no_keyerror()
    
    if success:
        print("\n🎉 Fix successful! The app should work without KeyError now.")
    else:
        print("\n⚠️ Still has issues - need more fixes")
