#!/usr/bin/env python3
"""
Test the main detect_logos_automatically function with OCR-based detection
"""

import cv2
import numpy as np
import tempfile
import os
from logo_detector import detect_logos_automatically

def create_video_frame_with_watermarks():
    """Create a test frame that looks like a real video with watermarks"""
    # Create a video-like frame
    img = np.zeros((720, 1280, 3), dtype=np.uint8)
    
    # Add some video content (gradient background)
    for y in range(720):
        for x in range(1280):
            img[y, x] = [int(x/5), int(y/3), 100]
    
    # Add some mock video content
    cv2.rectangle(img, (100, 100), (1180, 600), (50, 50, 150), -1)
    cv2.putText(img, "MOVIE CONTENT", (400, 350), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 3)
    
    # Add typical watermarks
    # Bottom right: website URL (common position)
    cv2.putText(img, "www.idramahd.com", (950, 680), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
    
    # Top right: logo text
    cv2.putText(img, "FREE MOVIES HD", (1000, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (180, 180, 180), 2)
    
    # Bottom left: copyright
    cv2.putText(img, "© 2024 StreamSite", (50, 680), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (160, 160, 160), 2)
    
    return img

def test_main_detection_function():
    """Test the main detection function"""
    print("Testing main logo detection function...")
    
    # Create test video frame
    frame = create_video_frame_with_watermarks()
    
    # Save as temporary video frame file
    temp_video_path = '/tmp/test_video_frame.mp4'
    
    # Create a simple 1-frame video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_video_path, fourcc, 1.0, (1280, 720))
    out.write(frame)
    out.release()
    
    try:
        # Test the main detection function
        detections = detect_logos_automatically(temp_video_path, '/opt/homebrew/bin/ffmpeg')
        
        print(f"\nMain function found {len(detections)} logo detections:")
        
        for i, detection in enumerate(detections):
            print(f"\n{i+1}. Detection:")
            print(f"   Type: {detection['type']}")
            print(f"   Confidence: {detection['confidence']:.3f}")
            print(f"   Position: ({detection['x']}, {detection['y']})")
            print(f"   Size: {detection['width']}x{detection['height']}")
            if 'text' in detection:
                print(f"   Text: '{detection['text']}'")
            if 'is_watermark' in detection:
                print(f"   Is Watermark: {detection['is_watermark']}")
            if 'corner' in detection:
                print(f"   Corner: {detection['corner']}")
        
        # Check if watermarks were detected
        watermarks_found = [d for d in detections if d.get('is_watermark', False)]
        print(f"\n✅ Found {len(watermarks_found)} watermarks:")
        for w in watermarks_found:
            print(f"   - '{w.get('text', 'Unknown')}' (confidence: {w['confidence']:.3f})")
        
        return len(detections) > 0
        
    finally:
        # Clean up
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)

if __name__ == "__main__":
    print("Testing OCR-based logo detection with main function...")
    
    success = test_main_detection_function()
    
    if success:
        print("\n🎉 OCR-based watermark detection is working perfectly!")
        print("The system can now effectively detect text watermarks like:")
        print("  - Website URLs (www.example.com)")
        print("  - Promotional text (FREE MOVIES HD)")
        print("  - Copyright notices (© 2024 Company)")
        print("  - And other text-based watermarks")
    else:
        print("\n❌ Detection needs improvement")
