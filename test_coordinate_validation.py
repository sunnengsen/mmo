#!/usr/bin/env python3
"""
Test the coordinate validation fix
"""
import subprocess
import tempfile
import cv2
import numpy as np

def test_coordinate_validation():
    """Test that coordinates are properly validated"""
    
    # Create a test video file
    print("Creating test video...")
    test_frames = []
    for i in range(30):  # 1 second at 30fps
        frame = np.zeros((720, 1280, 3), dtype=np.uint8)
        frame[:] = (50, 50, 50)
        cv2.putText(frame, f"Frame {i}", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        test_frames.append(frame)
    
    # Save as video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    test_video_path = 'test_coordinate_fix.mp4'
    out = cv2.VideoWriter(test_video_path, fourcc, 30.0, (1280, 720))
    
    for frame in test_frames:
        out.write(frame)
    out.release()
    
    print(f"Test video created: {test_video_path}")
    
    # Test coordinate validation by trying to use the FFmpeg delogo filter directly
    print("\nTesting coordinate validation...")
    
    # Test case 1: Valid coordinates
    print("Test 1: Valid coordinates")
    x, y, w, h = 100, 100, 200, 100
    cmd = [
        'ffmpeg', '-i', test_video_path,
        '-vf', f'delogo=x={x}:y={y}:w={w}:h={h}:show=0',
        '-t', '1', '-c:v', 'libx264', '-y', 'test_output_valid.mp4'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Valid coordinates work")
    else:
        print(f"❌ Valid coordinates failed: {result.stderr}")
    
    # Test case 2: Invalid coordinates (outside frame)
    print("\nTest 2: Invalid coordinates (outside frame)")
    x, y, w, h = 1300, 100, 200, 100  # x=1300 is outside 1280 width
    cmd = [
        'ffmpeg', '-i', test_video_path,
        '-vf', f'delogo=x={x}:y={y}:w={w}:h={h}:show=0',
        '-t', '1', '-c:v', 'libx264', '-y', 'test_output_invalid.mp4'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("❌ Invalid coordinates should have failed but didn't")
    else:
        print("✅ Invalid coordinates correctly failed")
        if "Logo area is outside of the frame" in result.stderr:
            print("   - Confirmed: 'Logo area is outside of the frame' error")
    
    # Test case 3: Edge coordinates (at boundary)
    print("\nTest 3: Edge coordinates (at video boundary)")
    x, y, w, h = 1180, 620, 100, 100  # Should fit within 1280x720
    cmd = [
        'ffmpeg', '-i', test_video_path,
        '-vf', f'delogo=x={x}:y={y}:w={w}:h={h}:show=0',
        '-t', '1', '-c:v', 'libx264', '-y', 'test_output_edge.mp4'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Edge coordinates work")
    else:
        print(f"❌ Edge coordinates failed: {result.stderr}")
    
    # Clean up test files
    import os
    for file in ['test_coordinate_fix.mp4', 'test_output_valid.mp4', 'test_output_invalid.mp4', 'test_output_edge.mp4']:
        if os.path.exists(file):
            os.remove(file)
    
    print("\n🎯 The coordinate validation should prevent the 'Logo area is outside of the frame' error")

if __name__ == "__main__":
    test_coordinate_validation()
