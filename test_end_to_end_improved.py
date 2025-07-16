#!/usr/bin/env python3
"""
End-to-end test to verify watermark detection and removal works
"""
import cv2
import numpy as np
import os
from logo_detector import detect_logos_automatically
from video_operations import VideoOperations

def test_end_to_end_watermark_removal():
    """Test the complete pipeline from detection to removal"""
    
    # Create a test video with watermark
    print("Creating test video with watermark...")
    
    # Create frames
    frames = []
    for i in range(10):  # 10 frames
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        frame[:] = (30, 30, 30)  # Dark background
        
        # Add some content
        cv2.rectangle(frame, (50, 50), (590, 430), (60, 60, 60), -1)
        cv2.putText(frame, f"Frame {i+1}", (300, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 2)
        
        # Add watermark in bottom-right corner
        watermark_text = "example.com"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        color = (255, 255, 255)
        thickness = 2
        
        (text_width, text_height), baseline = cv2.getTextSize(watermark_text, font, font_scale, thickness)
        x = 640 - text_width - 15
        y = 480 - 15
        
        cv2.putText(frame, watermark_text, (x, y), font, font_scale, color, thickness)
        frames.append(frame)
    
    # Save as video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('test_watermark_video.mp4', fourcc, 5.0, (640, 480))
    
    for frame in frames:
        out.write(frame)
    out.release()
    
    print("Test video created: test_watermark_video.mp4")
    
    # Test detection
    print("\nTesting watermark detection...")
    detections = detect_logos_automatically('test_watermark_video.mp4', 'ffmpeg')
    
    print(f"Detected {len(detections)} watermarks:")
    for i, det in enumerate(detections):
        print(f"  {i+1}. Area: {det['width']}x{det['height']} at ({det['x']}, {det['y']})")
        print(f"      Confidence: {det['confidence']:.2f}, Type: {det['type']}")
        if 'text' in det:
            print(f"      Text: \"{det['text']}\"")
    
    if not detections:
        print("❌ No watermarks detected!")
        return False
    
    # Test removal
    print("\nTesting watermark removal...")
    processor = VideoOperations('ffmpeg')
    
    # Process the video
    output_path = 'test_watermark_removed.mp4'
    success = processor.process_video(
        input_path='test_watermark_video.mp4',
        output_path=output_path,
        watermark_detections=detections,
        remove_watermarks=True
    )
    
    if success:
        print(f"✅ Video processed successfully: {output_path}")
        
        # Check if output file exists and has content
        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            print(f"✅ Output file has size: {os.path.getsize(output_path)} bytes")
            
            # Try to read the first frame to verify
            cap = cv2.VideoCapture(output_path)
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                print("✅ Can read processed video frames")
                # Save first frame for visual inspection
                cv2.imwrite('test_removed_frame.png', frame)
                print("First frame saved as 'test_removed_frame.png'")
                return True
            else:
                print("❌ Cannot read processed video frames")
                return False
        else:
            print("❌ Output file is empty or doesn't exist")
            return False
    else:
        print("❌ Video processing failed")
        return False

if __name__ == "__main__":
    success = test_end_to_end_watermark_removal()
    if success:
        print("\n🎉 End-to-end test PASSED!")
    else:
        print("\n❌ End-to-end test FAILED!")
