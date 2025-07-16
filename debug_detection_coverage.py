#!/usr/bin/env python3
"""
Debug script to check watermark detection coverage.
Tests whether the detection finds the full watermark area or just fragments.
"""
import os
import cv2
import numpy as np
from logo_detector import detect_logos_automatically

def create_test_image_with_watermark():
    """Create a test image with a watermark for testing detection."""
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Add a watermark text
    watermark_text = "TEST WATERMARK"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.2
    color = (255, 255, 255)
    thickness = 2
    
    # Get text size
    (text_width, text_height), baseline = cv2.getTextSize(watermark_text, font, font_scale, thickness)
    
    # Position watermark in top-right corner
    x = 640 - text_width - 20
    y = text_height + 20
    
    # Draw the watermark
    cv2.putText(img, watermark_text, (x, y), font, font_scale, color, thickness)
    
    # Add a semi-transparent background rectangle
    cv2.rectangle(img, (x-10, y-text_height-10), (x+text_width+10, y+baseline+10), (100, 100, 100), -1)
    cv2.putText(img, watermark_text, (x, y), font, font_scale, color, thickness)
    
    return img, (x-10, y-text_height-10, text_width+20, text_height+baseline+20)

def test_detection_coverage():
    """Test detection coverage on a known watermark."""
    print("Creating test image with watermark...")
    test_image, true_watermark_area = create_test_image_with_watermark()
    
    # Save test image
    test_image_path = "debug_watermark_detection.png"
    cv2.imwrite(test_image_path, test_image)
    
    true_x, true_y, true_w, true_h = true_watermark_area
    print(f"True watermark area: {true_w}x{true_h} at ({true_x}, {true_y})")
    
    # Test detection
    print("\nRunning watermark detection...")
    detections = detect_logos_automatically(test_image_path, 'ffmpeg')
    
    print(f"\nDetected {len(detections)} watermarks:")
    total_detected_area = 0
    
    for i, det in enumerate(detections):
        det_area = det['width'] * det['height']
        total_detected_area += det_area
        
        print(f"  {i+1}. Area: {det['width']}x{det['height']} at ({det['x']}, {det['y']})")
        print(f"      Pixel area: {det_area}")
        print(f"      Confidence: {det['confidence']:.2f}, Type: {det['type']}")
        if 'text' in det:
            print(f"      Text: \"{det['text']}\"")
        
        # Check overlap with true watermark area
        overlap_x = max(det['x'], true_x)
        overlap_y = max(det['y'], true_y)
        overlap_w = min(det['x'] + det['width'], true_x + true_w) - overlap_x
        overlap_h = min(det['y'] + det['height'], true_y + true_h) - overlap_y
        
        if overlap_w > 0 and overlap_h > 0:
            overlap_area = overlap_w * overlap_h
            coverage = overlap_area / (true_w * true_h) * 100
            print(f"      Coverage of true watermark: {coverage:.1f}%")
        else:
            print(f"      No overlap with true watermark")
    
    true_area = true_w * true_h
    print(f"\nTrue watermark area: {true_area} pixels")
    print(f"Total detected area: {total_detected_area} pixels")
    print(f"Coverage ratio: {total_detected_area / true_area * 100:.1f}%")
    
    # Visual debug - draw detected areas on image
    debug_image = test_image.copy()
    
    # Draw true watermark area in green
    cv2.rectangle(debug_image, (true_x, true_y), (true_x + true_w, true_y + true_h), (0, 255, 0), 2)
    cv2.putText(debug_image, "TRUE", (true_x, true_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    # Draw detected areas in red
    for i, det in enumerate(detections):
        x, y, w, h = det['x'], det['y'], det['width'], det['height']
        cv2.rectangle(debug_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(debug_image, f"DET{i+1}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    
    cv2.imwrite("debug_detection_coverage.png", debug_image)
    print(f"\nDebug image saved as 'debug_detection_coverage.png'")
    print("Green rectangle: True watermark area")
    print("Red rectangles: Detected areas")
    
    # Clean up
    if os.path.exists(test_image_path):
        os.remove(test_image_path)

if __name__ == "__main__":
    test_detection_coverage()
