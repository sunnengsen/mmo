#!/usr/bin/env python3
"""
Debug watermark detection to see what's being found
"""

import cv2
import numpy as np
import sys
sys.path.append('.')
from logo_detector import LogoDetector

def debug_detection():
    """Debug what the detection is finding"""
    print("🔍 Debugging watermark detection...")
    
    # Create test image with clear watermarks
    img = np.zeros((720, 1280, 3), dtype=np.uint8)
    img[:] = (40, 40, 40)  # Dark background
    
    # Add video content
    cv2.rectangle(img, (100, 100), (1180, 600), (60, 60, 120), -1)
    cv2.putText(img, "VIDEO CONTENT", (400, 350), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    
    # Add watermarks that should be detected
    cv2.putText(img, "www.dramahd.com", (950, 680), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
    cv2.putText(img, "FREE HD MOVIES", (1000, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (180, 180, 180), 2)
    
    # Save for visual inspection
    cv2.imwrite('debug_watermark_test.png', img)
    print("✅ Test image saved as debug_watermark_test.png")
    
    # Test detection
    detector = LogoDetector('ffmpeg')
    
    # Test corner detection
    print("\n1. Testing corner detection...")
    corner_detections = detector.detect_logos_in_corners(img)
    print(f"Found {len(corner_detections)} corner detections")
    
    for i, detection in enumerate(corner_detections):
        print(f"  Detection {i+1}:")
        print(f"    Type: {detection.get('type', 'unknown')}")
        print(f"    Corner: {detection.get('corner', 'N/A')}")
        print(f"    Text: '{detection.get('text', 'N/A')}'")
        print(f"    Watermark: {detection.get('is_watermark', False)}")
        print(f"    Confidence: {detection.get('confidence', 0):.3f}")
        print()
    
    # Test OCR detection directly
    print("\n2. Testing OCR detection...")
    ocr_detections = detector._detect_text_with_ocr(img, 0, 0)
    print(f"Found {len(ocr_detections)} OCR detections")
    
    for i, detection in enumerate(ocr_detections):
        print(f"  OCR Detection {i+1}:")
        print(f"    Text: '{detection.get('text', 'N/A')}'")
        print(f"    Watermark: {detection.get('is_watermark', False)}")
        print(f"    Confidence: {detection.get('confidence', 0):.3f}")
        print()
    
    # Test watermark text checker directly
    print("\n3. Testing watermark text checker...")
    test_texts = [
        "www.dramahd.com",
        "FREE HD MOVIES", 
        "VIDEO CONTENT",
        "Download Free Movies",
        "Watch HD Stream"
    ]
    
    for text in test_texts:
        is_watermark = detector._is_watermark_text(text)
        print(f"  '{text}' -> Watermark: {is_watermark}")

if __name__ == "__main__":
    debug_detection()
