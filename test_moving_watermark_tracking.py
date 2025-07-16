#!/usr/bin/env python3
"""
Test script for moving watermark tracking and position-aware removal.
This will test the enhanced system that can track watermarks through their movement
and apply removal at different positions throughout the video.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logo_detector import LogoDetector
import cv2
import numpy as np

def test_moving_watermark_tracking():
    """Test the moving watermark tracking system"""
    print("🎬 Testing Moving Watermark Tracking System")
    print("=" * 50)
    
    # Test with sample video
    test_video = "test_watermark_video.mp4"
    
    if not os.path.exists(test_video):
        print(f"❌ Test video not found: {test_video}")
        print("Please ensure you have a test video with moving watermarks.")
        return
    
    # Initialize detector
    detector = LogoDetector()
    
    # Test moving watermark detection with position tracking
    print("\n1. Testing moving watermark detection with position tracking...")
    
    # Detect watermarks with position information
    detected_logos = detector.detect_logos_from_video(test_video)
    
    if not detected_logos:
        print("❌ No watermarks detected")
        return
    
    print(f"✅ Found {len(detected_logos)} watermark detections")
    
    # Analyze movement patterns
    print("\n2. Analyzing movement patterns...")
    
    # Group detections by similar text content
    text_groups = {}
    for logo in detected_logos:
        text = logo.get('text', '').strip()
        if text:
            if text not in text_groups:
                text_groups[text] = []
            text_groups[text].append(logo)
    
    print(f"Found {len(text_groups)} unique text watermarks:")
    
    moving_watermarks = []
    for text, detections in text_groups.items():
        if len(detections) > 1:
            # This is a moving watermark
            positions = [(d['x'], d['y']) for d in detections]
            position_variance = np.var(positions, axis=0)
            
            print(f"  📍 '{text[:30]}...' - {len(detections)} positions")
            print(f"      Position variance: X={position_variance[0]:.1f}, Y={position_variance[1]:.1f}")
            
            if position_variance[0] > 100 or position_variance[1] > 100:
                moving_watermarks.append({
                    'text': text,
                    'detections': detections,
                    'movement_type': 'significant_movement'
                })
                print(f"      ✅ Classified as MOVING watermark")
            else:
                print(f"      ⚪ Classified as STATIC watermark (minor position variation)")
        else:
            print(f"  📍 '{text[:30]}...' - 1 position (static)")
    
    print(f"\n3. Found {len(moving_watermarks)} truly moving watermarks")
    
    # Test position tracking for each moving watermark
    for i, watermark in enumerate(moving_watermarks):
        print(f"\n4.{i+1} Analyzing movement pattern for '{watermark['text'][:20]}...'")
        
        detections = watermark['detections']
        
        # Sort by frame_time if available
        if 'frame_time' in detections[0]:
            detections.sort(key=lambda x: x['frame_time'])
        
        # Calculate movement path
        positions = [(d['x'], d['y']) for d in detections]
        times = [d.get('frame_time', i) for i, d in enumerate(detections)]
        
        print(f"     Movement path ({len(positions)} points):")
        for j, (pos, time) in enumerate(zip(positions, times)):
            print(f"       {j+1}. Time {time:.2f}s: ({pos[0]}, {pos[1]})")
        
        # Calculate movement characteristics
        x_coords = [pos[0] for pos in positions]
        y_coords = [pos[1] for pos in positions]
        
        x_range = max(x_coords) - min(x_coords)
        y_range = max(y_coords) - min(y_coords)
        
        print(f"     Movement range: X={x_range}px, Y={y_range}px")
        
        # Determine movement type
        if x_range > y_range * 2:
            movement_type = "horizontal"
        elif y_range > x_range * 2:
            movement_type = "vertical"
        else:
            movement_type = "diagonal/circular"
        
        print(f"     Movement type: {movement_type}")
        
        # Test position interpolation
        if len(detections) >= 2:
            print(f"     Testing position interpolation...")
            
            # Create position timeline
            position_timeline = []
            for j in range(len(detections) - 1):
                start_pos = positions[j]
                end_pos = positions[j + 1]
                start_time = times[j]
                end_time = times[j + 1]
                
                # Interpolate positions between keyframes
                time_diff = end_time - start_time
                if time_diff > 0:
                    steps = max(1, int(time_diff * 10))  # 10 positions per second
                    for step in range(steps):
                        t = step / steps
                        interp_x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
                        interp_y = start_pos[1] + (end_pos[1] - start_pos[1]) * t
                        interp_time = start_time + time_diff * t
                        
                        position_timeline.append({
                            'time': interp_time,
                            'x': int(interp_x),
                            'y': int(interp_y),
                            'width': detections[j]['width'],
                            'height': detections[j]['height']
                        })
            
            print(f"     Created {len(position_timeline)} interpolated positions")
            
            # Show sample interpolated positions
            if position_timeline:
                print(f"     Sample interpolated positions:")
                for k, pos in enumerate(position_timeline[:5]):
                    print(f"       Time {pos['time']:.2f}s: ({pos['x']}, {pos['y']})")
                if len(position_timeline) > 5:
                    print(f"       ... and {len(position_timeline) - 5} more")
    
    print("\n5. Testing position-aware removal strategy...")
    
    # For each moving watermark, create a removal strategy
    for i, watermark in enumerate(moving_watermarks):
        print(f"\n5.{i+1} Removal strategy for '{watermark['text'][:20]}...'")
        
        detections = watermark['detections']
        
        # Strategy 1: Temporal segmentation
        print("     Strategy 1: Temporal segmentation")
        print("     - Divide video into segments based on watermark position")
        print("     - Apply different removal coordinates for each segment")
        
        # Strategy 2: Dynamic tracking
        print("     Strategy 2: Dynamic position tracking")
        print("     - Track watermark position throughout video")
        print("     - Apply removal filter with time-based position changes")
        
        # Strategy 3: Path-based removal
        print("     Strategy 3: Path-based removal")
        print("     - Create a removal path that follows the watermark movement")
        print("     - Use advanced FFmpeg filters for dynamic masking")
    
    print("\n✅ Moving watermark tracking test completed!")
    print("This test analyzed the movement patterns and prepared removal strategies.")
    
    return moving_watermarks

if __name__ == "__main__":
    test_moving_watermark_tracking()
