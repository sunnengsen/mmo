#!/usr/bin/env python3
"""
Simple test using a saved image to verify OCR detection
"""

import cv2
import numpy as np
from logo_detector import LogoDetector

def test_direct_detection():
    """Test detection directly on an image"""
    print("Testing direct OCR detection on image...")
    
    # Create test image with watermarks
    img = np.zeros((720, 1280, 3), dtype=np.uint8)
    img[:] = (40, 40, 40)  # Dark background
    
    # Add main content
    cv2.rectangle(img, (100, 100), (1180, 600), (60, 60, 120), -1)
    cv2.putText(img, "VIDEO CONTENT", (400, 350), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    
    # Add watermarks in typical positions
    cv2.putText(img, "www.idramahd.com", (950, 680), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
    cv2.putText(img, "FREE MOVIES HD", (1000, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (180, 180, 180), 2)
    
    # Save test image
    cv2.imwrite('/tmp/test_watermark_image.png', img)
    
    # Initialize detector
    detector = LogoDetector('/opt/homebrew/bin/ffmpeg')
    
    # Test full frame OCR
    print("\n1. Testing full frame OCR...")
    full_frame_detections = detector._detect_text_watermarks_full_frame(img)
    print(f"Full frame OCR found {len(full_frame_detections)} detections:")
    
    for i, det in enumerate(full_frame_detections):
        print(f"  {i+1}. {det['type']}: '{det.get('text', 'N/A')}' - Watermark: {det.get('is_watermark', False)} - Confidence: {det['confidence']:.3f}")
    
    # Test corner detection
    print("\n2. Testing corner detection...")
    corner_detections = detector.detect_logos_in_corners(img)
    ocr_corner_detections = [d for d in corner_detections if d['type'].startswith('ocr_')]
    print(f"Corner OCR found {len(ocr_corner_detections)} OCR detections:")
    
    for i, det in enumerate(ocr_corner_detections):
        print(f"  {i+1}. {det['type']}: '{det.get('text', 'N/A')}' - Watermark: {det.get('is_watermark', False)} - Confidence: {det['confidence']:.3f}")
    
    # Test specific regions
    print("\n3. Testing specific regions...")
    
    # Bottom right corner (where www.idramahd.com should be)
    h, w = img.shape[:2]
    bottom_right = img[int(h*0.75):h, int(w*0.6):w]
    br_detections = detector._detect_text_with_ocr(bottom_right, int(w*0.6), int(h*0.75))
    print(f"Bottom right OCR found {len(br_detections)} detections:")
    
    for i, det in enumerate(br_detections):
        print(f"  {i+1}. {det['type']}: '{det.get('text', 'N/A')}' - Watermark: {det.get('is_watermark', False)} - Confidence: {det['confidence']:.3f}")
    
    # Top right corner (where FREE MOVIES HD should be)
    top_right = img[0:int(h*0.25), int(w*0.6):w]
    tr_detections = detector._detect_text_with_ocr(top_right, int(w*0.6), 0)
    print(f"Top right OCR found {len(tr_detections)} detections:")
    
    for i, det in enumerate(tr_detections):
        print(f"  {i+1}. {det['type']}: '{det.get('text', 'N/A')}' - Watermark: {det.get('is_watermark', False)} - Confidence: {det['confidence']:.3f}")
    
    # Summary
    all_detections = full_frame_detections + corner_detections
    watermarks = [d for d in all_detections if d.get('is_watermark', False)]
    
    print(f"\n📊 Summary:")
    print(f"Total detections: {len(all_detections)}")
    print(f"Watermarks found: {len(watermarks)}")
    
    if watermarks:
        print("✅ Watermarks detected:")
        for w in watermarks:
            print(f"  - '{w.get('text', 'Unknown')}' (confidence: {w['confidence']:.3f})")
        return True
    else:
        print("❌ No watermarks detected")
        return False

if __name__ == "__main__":
    success = test_direct_detection()
    
    if success:
        print("\n🎉 OCR watermark detection is working!")
    else:
        print("\n⚠️  Need to investigate OCR detection")
