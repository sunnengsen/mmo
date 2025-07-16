#!/usr/bin/env python3
"""
Simple test script to check OCR functionality
"""

import cv2
import numpy as np
from logo_detector import LogoDetector

def test_ocr():
    # Create a simple test image with text
    img = np.zeros((200, 600, 3), dtype=np.uint8)
    
    # Add white text on black background
    cv2.putText(img, 'www.idramahd.com', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Save test image
    cv2.imwrite('test_watermark.png', img)
    print("Created test image: test_watermark.png")
    
    # Test with LogoDetector
    detector = LogoDetector('ffmpeg')  # ffmpeg path doesn't matter for this test
    
    # Test OCR detection
    detections = detector._detect_text_with_ocr(img, 0, 0)
    
    print(f"Found {len(detections)} detections:")
    for i, detection in enumerate(detections):
        print(f"  Detection {i+1}:")
        print(f"    Text: '{detection.get('text', 'N/A')}'")
        print(f"    Confidence: {detection.get('confidence', 0):.2f}")
        print(f"    Position: ({detection['x']}, {detection['y']}) Size: {detection['width']}x{detection['height']}")
        print(f"    Type: {detection.get('type', 'N/A')}")
        print(f"    Is watermark: {detection.get('is_watermark', False)}")
        print()

if __name__ == "__main__":
    test_ocr()
