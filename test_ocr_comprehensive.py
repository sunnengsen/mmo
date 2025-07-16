#!/usr/bin/env python3
"""
Comprehensive test for OCR-based logo detection
"""

import cv2
import numpy as np
from logo_detector import LogoDetector
import tempfile
import os

def create_test_watermark_image():
    """Create a test image with watermark text"""
    # Create a dark background image
    img = np.zeros((400, 600, 3), dtype=np.uint8)
    img[:] = (20, 20, 20)  # Dark background
    
    # Add some sample content
    cv2.rectangle(img, (50, 50), (550, 150), (100, 100, 100), -1)
    cv2.putText(img, "Sample Video Content", (60, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Add watermark text in corner (like www.idramahd.com)
    cv2.putText(img, "www.idramahd.com", (400, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
    
    # Add another watermark in different position
    cv2.putText(img, "FREE MOVIES HD", (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 2)
    
    return img

def test_ocr_detection():
    """Test OCR detection with sample watermark image"""
    print("Testing OCR-based watermark detection...")
    
    # Create test image
    test_img = create_test_watermark_image()
    
    # Save temporarily
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        temp_path = temp_file.name
        cv2.imwrite(temp_path, test_img)
    
    try:
        # Initialize detector
        detector = LogoDetector('/opt/homebrew/bin/ffmpeg')  # Adjust path as needed
        
        # Test OCR detection methods directly
        print("\n1. Testing OCR detection methods...")
        
        # Test corner detection
        detections = detector.detect_logos_in_corners(test_img)
        print(f"Corner detection found {len(detections)} items:")
        for i, det in enumerate(detections):
            print(f"  {i+1}. Type: {det['type']}, Confidence: {det['confidence']:.3f}")
            if 'text' in det:
                print(f"      Text: '{det['text']}'")
                print(f"      Watermark: {det.get('is_watermark', False)}")
            print(f"      Position: ({det['x']}, {det['y']}) Size: {det['width']}x{det['height']}")
        
        # Test full frame OCR scan
        print("\n2. Testing full frame OCR scan...")
        full_frame_detections = detector._detect_text_watermarks_full_frame(test_img)
        print(f"Full frame detection found {len(full_frame_detections)} items:")
        for i, det in enumerate(full_frame_detections):
            print(f"  {i+1}. Type: {det['type']}, Confidence: {det['confidence']:.3f}")
            if 'text' in det:
                print(f"      Text: '{det['text']}'")
                print(f"      Watermark: {det.get('is_watermark', False)}")
            print(f"      Position: ({det['x']}, {det['y']}) Size: {det['width']}x{det['height']}")
        
        # Test OCR directly on regions
        print("\n3. Testing OCR on bottom-right corner...")
        h, w = test_img.shape[:2]
        bottom_right = test_img[int(h*0.75):h, int(w*0.6):w]
        
        ocr_detections = detector._detect_text_with_ocr(bottom_right, int(w*0.6), int(h*0.75))
        print(f"OCR detection found {len(ocr_detections)} items:")
        for i, det in enumerate(ocr_detections):
            print(f"  {i+1}. Type: {det['type']}, Confidence: {det['confidence']:.3f}")
            if 'text' in det:
                print(f"      Text: '{det['text']}'")
                print(f"      Watermark: {det.get('is_watermark', False)}")
            print(f"      Position: ({det['x']}, {det['y']}) Size: {det['width']}x{det['height']}")
        
        # Save debug image
        debug_img = test_img.copy()
        
        # Draw detection boxes
        all_detections = detections + full_frame_detections + ocr_detections
        for det in all_detections:
            color = (0, 255, 0) if det.get('is_watermark', False) else (0, 0, 255)
            cv2.rectangle(debug_img, (det['x'], det['y']), 
                         (det['x'] + det['width'], det['y'] + det['height']), color, 2)
            
            # Add label
            label = f"{det['type']}: {det['confidence']:.2f}"
            if 'text' in det:
                label += f" '{det['text'][:15]}'"
            cv2.putText(debug_img, label, (det['x'], det['y']-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        debug_path = '/Users/sunnengsen/Documents/Code/script_mmo/debug_ocr_detection.png'
        cv2.imwrite(debug_path, debug_img)
        print(f"\nDebug image saved to: {debug_path}")
        
        return len(all_detections) > 0
        
    finally:
        # Clean up
        os.unlink(temp_path)

def test_with_different_watermarks():
    """Test with different types of watermarks"""
    print("\n" + "="*50)
    print("Testing with different watermark types...")
    
    # Test different watermark styles
    watermark_texts = [
        "www.example.com",
        "FREE MOVIES",
        "SUBSCRIBE NOW",
        "HD QUALITY",
        "© 2024 Company",
        "WATERMARK",
        "idramahd.com"
    ]
    
    detector = LogoDetector('/opt/homebrew/bin/ffmpeg')
    
    for text in watermark_texts:
        print(f"\nTesting watermark: '{text}'")
        
        # Create test image
        img = np.zeros((200, 400, 3), dtype=np.uint8)
        img[:] = (30, 30, 30)
        
        # Add watermark
        cv2.putText(img, text, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
        
        # Test detection
        detections = detector.detect_logos_in_corners(img)
        watermark_found = any(det.get('is_watermark', False) for det in detections)
        
        print(f"  Watermark detected: {watermark_found}")
        if detections:
            for det in detections:
                if 'text' in det:
                    print(f"    OCR result: '{det['text']}' (confidence: {det['confidence']:.3f})")

if __name__ == "__main__":
    # Configure Python environment first
    import sys
    sys.path.append('/Users/sunnengsen/Documents/Code/script_mmo')
    
    print("Starting comprehensive OCR watermark detection test...")
    
    success = test_ocr_detection()
    test_with_different_watermarks()
    
    if success:
        print("\n✅ OCR detection is working!")
    else:
        print("\n❌ OCR detection has issues")
