#!/usr/bin/env python3
"""
Test and debug current moving watermark grouping
"""

import sys
import os
sys.path.append('/Users/sunnengsen/Documents/Code/script_mmo')

from logo_detector import LogoDetector

def test_grouping():
    print("Testing current watermark grouping on moving watermark video...")
    
    # Initialize detector
    detector = LogoDetector('/opt/homebrew/bin/ffmpeg')
    
    # Test video
    video_path = '/Users/sunnengsen/Documents/Code/script_mmo/test_moving_final.mp4'
    
    # Run detection
    result = detector.detect_logos_with_timeline(video_path)
    
    print(f"\nDetection results:")
    print(f"Total watermarks found: {len(result)}")
    
    for i, watermark in enumerate(result):
        print(f"\nWatermark {i+1}:")
        print(f"  Text: '{watermark.get('text', '')}'")
        print(f"  Type: {watermark.get('type', 'unknown')}")
        print(f"  Moving: {watermark.get('is_moving', False)}")
        print(f"  Confidence: {watermark.get('confidence', 0):.2f}")
        print(f"  Detections: {len(watermark.get('detections', []))}")
        print(f"  Movement variance: x={watermark.get('movement_analysis', {}).get('x_variance', 0):.1f}, y={watermark.get('movement_analysis', {}).get('y_variance', 0):.1f}")
        
        # Show first few detections
        detections = watermark.get('detections', [])
        if detections:
            print(f"  Sample detections:")
            for j, detection in enumerate(detections[:3]):
                print(f"    {j+1}. '{detection.get('text', '')}' at ({detection['x']}, {detection['y']}) conf={detection.get('confidence', 0):.2f}")
            if len(detections) > 3:
                print(f"    ... and {len(detections) - 3} more")
    
    # Now test the fuzzy grouping logic directly
    print("\n\nTesting fuzzy text grouping:")
    
    # Test cases for moving watermark fragments
    test_cases = [
        ("MOV", "MOVING"),
        ("MOVING", "WATERMARK"),
        ("WATER", "WATERMARK"),
        ("MARK", "WATERMARK"),
        ("MOV", "MARK"),
        ("MOVING", "MOV"),
        ("WATERMARK", "EMARK"),
        ("VING", "MOVING"),
        ("WATER", "ATER"),
        ("LOGO", "BRAND"),
        ("©", "COPYRIGHT"),
        ("®", "REGISTERED"),
        ("™", "TRADEMARK"),
        ("UNRELATED", "DIFFERENT"),
        ("ABC", "XYZ"),
        ("MOVING", "LOGO"),
        ("WATERMARK", "LOGO"),
    ]
    
    for text1, text2 in test_cases:
        similar = detector._texts_are_similar(text1, text2)
        print(f"'{text1}' vs '{text2}': {'Similar' if similar else 'Different'}")

if __name__ == "__main__":
    test_grouping()
