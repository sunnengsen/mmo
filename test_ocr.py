#!/usr/bin/env python3
"""
Test OCR-based text detection
"""

import cv2
import numpy as np
from logo_detector import LogoDetector

def test_ocr():
    """Test OCR detection functionality"""
    
    # Create a simple test image with text
    img = np.ones((200, 600, 3), dtype=np.uint8) * 255  # White background
    
    # Add text watermark
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, 'www.idramahd.com', (50, 100), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(img, 'Watch Free Movies', (50, 150), font, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
    
    # Initialize detector
    detector = LogoDetector('/usr/local/bin/ffmpeg')  # Adjust path as needed
    
    # Test OCR detection
    print("Testing OCR-based text detection...")
    detections = detector._detect_text_with_ocr(img, 0, 0)
    
    print(f"Found {len(detections)} text detections:")
    for i, detection in enumerate(detections):
        print(f"  Detection {i+1}:")
        print(f"    Text: '{detection.get('text', 'N/A')}'")
        print(f"    Position: ({detection['x']}, {detection['y']}, {detection['width']}, {detection['height']})")
        print(f"    Confidence: {detection['confidence']:.3f}")
        print(f"    Type: {detection['type']}")
        print(f"    Is watermark: {detection.get('is_watermark', False)}")
        print()
    
    return detections

if __name__ == "__main__":
    detections = test_ocr()
    if detections:
        print("✅ OCR detection working successfully!")
    else:
        print("⚠️ No detections found - OCR may need adjustment")
