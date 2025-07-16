#!/usr/bin/env python3
"""
Test OCR detection with a real video scenario
"""

import cv2
import numpy as np
from logo_detector import detect_logos_automatically

def test_with_sample_video():
    # Create a more realistic test scenario
    # Simulate a video frame with a watermark in the bottom right corner
    img = np.random.randint(0, 255, (720, 1280, 3), dtype=np.uint8)  # Random video-like background
    
    # Add a semi-transparent watermark in the bottom right
    overlay = img.copy()
    cv2.rectangle(overlay, (1000, 650), (1270, 710), (50, 50, 50), -1)  # Dark background
    cv2.putText(overlay, 'www.idramahd.com', (1010, 685), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # Blend the overlay
    img = cv2.addWeighted(img, 0.7, overlay, 0.3, 0)
    
    # Save test image
    cv2.imwrite('test_video_frame.png', img)
    print("Created test video frame: test_video_frame.png")
    
    # Test with the main detection function
    # Since we can't use a real video, let's test the detection directly
    from logo_detector import LogoDetector
    
    detector = LogoDetector('ffmpeg')  # ffmpeg path doesn't matter for this test
    
    # Test corner detection
    detections = detector.detect_logos_in_corners(img)
    
    print(f"Found {len(detections)} detections in corners:")
    for i, detection in enumerate(detections):
        print(f"  Detection {i+1}:")
        print(f"    Text: '{detection.get('text', 'N/A')}'")
        print(f"    Confidence: {detection.get('confidence', 0):.2f}")
        print(f"    Position: ({detection['x']}, {detection['y']}) Size: {detection['width']}x{detection['height']}")
        print(f"    Type: {detection.get('type', 'N/A')}")
        print(f"    Corner: {detection.get('corner', 'N/A')}")
        print(f"    Is watermark: {detection.get('is_watermark', False)}")
        print()
    
    # Test full frame detection
    full_frame_detections = detector._detect_text_watermarks_full_frame(img)
    
    print(f"Found {len(full_frame_detections)} full frame detections:")
    for i, detection in enumerate(full_frame_detections):
        print(f"  Detection {i+1}:")
        print(f"    Text: '{detection.get('text', 'N/A')}'")
        print(f"    Confidence: {detection.get('confidence', 0):.2f}")
        print(f"    Position: ({detection['x']}, {detection['y']}) Size: {detection['width']}x{detection['height']}")
        print(f"    Type: {detection.get('type', 'N/A')}")
        print(f"    Is watermark: {detection.get('is_watermark', False)}")
        print()

if __name__ == "__main__":
    test_with_sample_video()
