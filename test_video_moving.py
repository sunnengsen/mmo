#!/usr/bin/env python3
"""
Test the moving watermark detection with video simulation
"""

import cv2
import numpy as np
import sys
import time
import tempfile
import os
sys.path.append('.')

def create_test_video_with_moving_watermark():
    """Create a test video with a moving watermark"""
    print("🎬 Creating test video with moving watermark...")
    
    # Video properties
    fps = 1  # 1 FPS for quick testing
    duration = 5  # 5 seconds
    width, height = 1280, 720
    
    # Create temporary video file
    temp_video = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
    temp_video.close()
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_video.name, fourcc, fps, (width, height))
    
    # Watermark positions (moving from top-left to bottom-right)
    positions = [
        (50, 50),      # Frame 1: top-left
        (200, 100),    # Frame 2: moving right
        (400, 200),    # Frame 3: center-left
        (600, 300),    # Frame 4: center-right
        (1000, 650),   # Frame 5: bottom-right
    ]
    
    for frame_num, (wx, wy) in enumerate(positions):
        # Create frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:] = (30, 30, 30)  # Dark background
        
        # Add main content
        cv2.rectangle(frame, (100, 100), (1180, 620), (50, 50, 100), -1)
        cv2.putText(frame, f"VIDEO FRAME {frame_num + 1}", (400, 350), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
        
        # Add moving watermark
        cv2.putText(frame, "www.testsite.com", (wx, wy), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
        
        # Add another static watermark for comparison
        cv2.putText(frame, "HD QUALITY", (1100, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 2)
        
        # Write frame
        out.write(frame)
    
    out.release()
    print(f"✅ Test video created: {temp_video.name}")
    return temp_video.name

def test_moving_watermark_detection():
    """Test the enhanced detection on moving watermarks"""
    
    # Create test video
    video_path = create_test_video_with_moving_watermark()
    
    try:
        print(f"\n🔍 Testing moving watermark detection...")
        
        from logo_detector import detect_logos_automatically
        
        # Test the enhanced detection
        start_time = time.time()
        result = detect_logos_automatically(video_path, '/opt/homebrew/bin/ffmpeg')
        detection_time = time.time() - start_time
        
        print(f"\n📊 DETECTION RESULTS:")
        print(f"  ⏱️  Detection time: {detection_time:.2f}s")
        print(f"  🎯 Total detections: {len(result)}")
        
        # Analyze results
        watermarks = [r for r in result if r.get('is_watermark', False)]
        text_detections = [r for r in result if r.get('text', '').strip()]
        
        print(f"  💧 Watermarks found: {len(watermarks)}")
        print(f"  📝 Text detections: {len(text_detections)}")
        
        if result:
            print(f"\n🔍 DETAILED RESULTS:")
            for i, det in enumerate(result[:5]):  # Show top 5
                text = det.get('text', 'N/A')
                corner = det.get('corner', 'N/A')
                is_watermark = det.get('is_watermark', False)
                confidence = det.get('confidence', 0)
                frame = det.get('frame', 'N/A')
                multi_frame = det.get('multi_frame', False)
                
                print(f"    {i+1}. \"{text}\"")
                print(f"       Position: {corner}")
                print(f"       Watermark: {is_watermark}")
                print(f"       Confidence: {confidence:.3f}")
                print(f"       Frame: {frame}")
                print(f"       Multi-frame: {multi_frame}")
                print()
        
        # Success criteria
        has_watermarks = len(watermarks) > 0
        has_moving_detection = any(det.get('multi_frame', False) for det in result)
        fast_enough = detection_time < 30  # Should be under 30 seconds
        
        print(f"📈 SUCCESS METRICS:")
        print(f"  ✅ Found watermarks: {'YES' if has_watermarks else 'NO'}")
        print(f"  ✅ Multi-frame detection: {'YES' if has_moving_detection else 'NO'}")
        print(f"  ✅ Fast enough: {'YES' if fast_enough else 'NO'}")
        
        success = has_watermarks and fast_enough
        
        if success:
            print(f"\n🎉 MOVING WATERMARK DETECTION WORKING!")
            print(f"   Your app can now handle watermarks that move position.")
        else:
            print(f"\n⚠️  NEEDS IMPROVEMENT")
            if not has_watermarks:
                print(f"     - No watermarks detected")
            if not fast_enough:
                print(f"     - Detection too slow ({detection_time:.1f}s)")
        
        return success
        
    finally:
        # Clean up
        if os.path.exists(video_path):
            os.remove(video_path)
            print(f"🧹 Cleaned up test video")

if __name__ == "__main__":
    test_moving_watermark_detection()
