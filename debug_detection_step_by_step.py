#!/usr/bin/env python3
"""
Debug the detection and grouping process step by step
"""

import sys
import os
sys.path.append('/Users/sunnengsen/Documents/Code/script_mmo')

from logo_detector import LogoDetector
import cv2

def debug_detection_process():
    print("Debugging detection process step by step...")
    
    # Initialize detector
    detector = LogoDetector('/opt/homebrew/bin/ffmpeg')
    
    # Test video
    video_path = '/Users/sunnengsen/Documents/Code/script_mmo/test_moving_final.mp4'
    
    # Manually walk through the detection process
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    
    print(f"Video info: {total_frames} frames, {fps:.2f} fps, {duration:.2f}s")
    
    # Sample a few frames manually
    sample_times = [0, 2.5, 5.0, 7.5, 10.0]
    all_detections = []
    
    for sample_time in sample_times:
        frame_number = int(sample_time * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        
        if not ret:
            print(f"Failed to read frame at {sample_time}s")
            continue
            
        print(f"\n--- Frame at {sample_time}s ---")
        
        # Run detection on this frame
        frame_detections = detector.detect_logos_in_corners(frame)
        
        print(f"Raw detections: {len(frame_detections)}")
        for i, det in enumerate(frame_detections):
            print(f"  {i+1}. '{det.get('text', '')}' at ({det['x']}, {det['y']}) conf={det.get('confidence', 0):.2f} watermark={det.get('is_watermark', False)}")
        
        # Add timestamp for timeline creation
        for det in frame_detections:
            det['timestamp'] = sample_time
            
        all_detections.extend(frame_detections)
    
    cap.release()
    
    print(f"\n--- Total raw detections: {len(all_detections)} ---")
    
    # Now test the timeline creation
    print("\n--- Testing timeline creation ---")
    timelines = detector._create_watermark_timelines(all_detections)
    
    print(f"Created {len(timelines)} timelines:")
    for i, timeline in enumerate(timelines):
        print(f"\nTimeline {i+1}:")
        print(f"  Text: '{timeline.get('text', '')}'")
        print(f"  Type: {timeline.get('type', 'unknown')}")
        print(f"  Detections: {len(timeline.get('detections', []))}")
        print(f"  Confidence: {timeline.get('confidence', 0):.2f}")
        
        # Show all detections in this timeline
        for j, det in enumerate(timeline.get('detections', [])):
            print(f"    {j+1}. '{det.get('text', '')}' at ({det['x']}, {det['y']}) t={det.get('timestamp', 0):.1f}s conf={det.get('confidence', 0):.2f}")
    
    # Test manual grouping of detected fragments
    print("\n--- Manual grouping test ---")
    
    # Extract all text fragments
    text_fragments = []
    for det in all_detections:
        text = det.get('text', '').strip()
        if text and len(text) >= 2:
            text_fragments.append(text)
    
    print(f"Text fragments found: {text_fragments}")
    
    # Try to group them manually
    groups = []
    for fragment in text_fragments:
        placed = False
        for group in groups:
            if any(detector._texts_are_similar(fragment, existing) for existing in group):
                group.append(fragment)
                placed = True
                break
        if not placed:
            groups.append([fragment])
    
    print(f"Manual grouping result:")
    for i, group in enumerate(groups):
        print(f"  Group {i+1}: {group}")

if __name__ == "__main__":
    debug_detection_process()
