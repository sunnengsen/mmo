#!/usr/bin/env python3
"""
Debug the detection process step by step to understand what's happening
"""
import cv2
import numpy as np
from logo_detector import LogoDetector

def debug_detection_process():
    """Debug the detection process step by step"""
    
    # Create a simple test image
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    img[:] = (50, 50, 50)
    
    # Add a watermark
    watermark_text = 'example.com'
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8
    color = (255, 255, 255)
    thickness = 2
    
    (text_width, text_height), baseline = cv2.getTextSize(watermark_text, font, font_scale, thickness)
    x = 640 - text_width - 15
    y = 480 - 15
    
    cv2.putText(img, watermark_text, (x, y), font, font_scale, color, thickness)
    cv2.imwrite('debug_test.png', img)
    
    print(f"True watermark: '{watermark_text}' at ({x}, {y-text_height}) size: {text_width}x{text_height}")
    
    # Test detection step by step
    detector = LogoDetector('ffmpeg')
    
    # Step 1: Corner detection
    corner_detections = detector.detect_logos_in_corners(img)
    print(f"\nStep 1 - Corner detections: {len(corner_detections)}")
    for i, det in enumerate(corner_detections):
        print(f"  {i+1}. {det['width']}x{det['height']} at ({det['x']}, {det['y']}) - {det['type']}")
        print(f"      Confidence: {det['confidence']:.2f}, Text: '{det.get('text', '')}'")
        print(f"      Corner: {det.get('corner', 'unknown')}")
    
    # Step 2: Full frame detection
    full_frame_detections = detector._detect_text_watermarks_full_frame(img)
    print(f"\nStep 2 - Full frame detections: {len(full_frame_detections)}")
    for i, det in enumerate(full_frame_detections):
        print(f"  {i+1}. {det['width']}x{det['height']} at ({det['x']}, {det['y']}) - {det['type']}")
        print(f"      Confidence: {det['confidence']:.2f}, Text: '{det.get('text', '')}'")
    
    # Step 3: Before merging
    all_detections = corner_detections + full_frame_detections
    print(f"\nStep 3 - All detections before merging: {len(all_detections)}")
    for i, det in enumerate(all_detections):
        print(f"  {i+1}. {det['width']}x{det['height']} at ({det['x']}, {det['y']}) - {det['type']}")
        print(f"      Confidence: {det['confidence']:.2f}, Text: '{det.get('text', '')}'")
    
    # Step 4: After merging
    merged_detections = detector.merge_overlapping_detections(all_detections)
    print(f"\nStep 4 - After merging: {len(merged_detections)}")
    for i, det in enumerate(merged_detections):
        print(f"  {i+1}. {det['width']}x{det['height']} at ({det['x']}, {det['y']}) - {det['type']}")
        print(f"      Confidence: {det['confidence']:.2f}, Text: '{det.get('text', '')}'")
    
    # Create visual debug image
    debug_img = img.copy()
    
    # Draw true watermark area in green
    cv2.rectangle(debug_img, (x, y-text_height), (x+text_width, y), (0, 255, 0), 2)
    cv2.putText(debug_img, "TRUE", (x, y-text_height-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    # Draw all detections before merging in blue
    for i, det in enumerate(all_detections):
        cv2.rectangle(debug_img, (det['x'], det['y']), (det['x']+det['width'], det['y']+det['height']), (255, 0, 0), 1)
        cv2.putText(debug_img, f"B{i+1}", (det['x'], det['y']-2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)
    
    # Draw merged detections in red
    for i, det in enumerate(merged_detections):
        cv2.rectangle(debug_img, (det['x'], det['y']), (det['x']+det['width'], det['y']+det['height']), (0, 0, 255), 2)
        cv2.putText(debug_img, f"M{i+1}", (det['x'], det['y']-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    
    cv2.imwrite('debug_detection_process.png', debug_img)
    print(f"\nVisual debug saved as 'debug_detection_process.png'")
    print("Green: True watermark area")
    print("Blue: Individual detections before merging")
    print("Red: Final merged detections")

if __name__ == "__main__":
    debug_detection_process()
