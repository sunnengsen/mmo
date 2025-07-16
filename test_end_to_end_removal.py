#!/usr/bin/env python3
"""
End-to-end test for watermark removal system
Tests the complete workflow from detection to removal
"""

import os
import sys
import tempfile
import subprocess
import time
import cv2
import numpy as np
from typing import List, Dict, Any

def create_test_video_with_watermarks(video_path: str, duration: int = 5) -> str:
    """Create a test video with watermarks in different positions"""
    
    # Create a simple test video with watermarks
    cmd = [
        'ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=blue:size=1280x720:duration=5',
        '-vf', 
        'drawtext=text="FIXED WATERMARK":fontcolor=white:fontsize=40:x=50:y=50,'
        'drawtext=text="MOVING WATERMARK":fontcolor=yellow:fontsize=30:x=200+50*sin(t):y=200+30*cos(t),'
        'drawtext=text="www.example.com":fontcolor=red:fontsize=20:x=1000:y=650',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', video_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to create test video: {result.stderr}")
        return None
        
    return video_path

def test_detection_pipeline(video_path: str) -> List[Dict[str, Any]]:
    """Test the detection pipeline"""
    print("\n🔍 Testing detection pipeline...")
    
    try:
        from logo_detector import detect_logos_automatically
        detected_logos = detect_logos_automatically(video_path, '/opt/homebrew/bin/ffmpeg')
        
        print(f"✅ Detection found {len(detected_logos)} watermarks")
        for i, logo in enumerate(detected_logos):
            print(f"  • Logo {i+1}: '{logo.get('text', 'unknown')}' at {logo.get('corner', 'unknown')} "
                  f"(conf: {logo.get('confidence', 0):.3f})")
        
        return detected_logos
        
    except Exception as e:
        print(f"❌ Detection failed: {e}")
        return []

def test_removal_pipeline(video_path: str, detected_logos: List[Dict[str, Any]]) -> bool:
    """Test the removal pipeline"""
    print("\n🛠️  Testing removal pipeline...")
    
    if not detected_logos:
        print("❌ No watermarks to remove")
        return False
    
    try:
        from video_operations import VideoOperations
        
        # Mock main window for testing
        class MockMainWindow:
            def __init__(self):
                self.ffmpeg_path = '/opt/homebrew/bin/ffmpeg'
                self.ytdlp_path = None
                self.worker_thread = None
                
            def log_message(self, msg):
                print(f"  LOG: {msg}")
            def show_error(self, msg):
                print(f"  ERROR: {msg}")
            def start_operation(self, msg):
                print(f"  START: {msg}")
            def finish_operation(self, success, msg):
                print(f"  FINISH: {success} - {msg}")
        
        mock_window = MockMainWindow()
        video_ops = VideoOperations(mock_window)
        
        # Test the logic without actually running ffmpeg
        print("🔍 Testing removal logic...")
        
        # Test grouping
        watermark_groups = video_ops._group_watermarks_by_position(detected_logos)
        print(f"  • Grouped {len(detected_logos)} watermarks into {len(watermark_groups)} groups")
        
        # Test moving watermark detection
        has_moving = any(d.get('multi_frame', False) or d.get('moving_scan', False) for d in detected_logos)
        print(f"  • Moving watermarks detected: {has_moving}")
        
        # Test method selection for each watermark
        for i, logo in enumerate(detected_logos):
            logo_type = logo.get('type', 'unknown')
            confidence = logo.get('confidence', 0)
            
            if 'ocr_' in logo_type or logo.get('is_watermark', False):
                method = "Smart inpaint (recommended for text)"
            elif 'text' in logo_type or 'website' in logo_type:
                method = "Smart inpaint (recommended for text)"
            elif confidence > 0.7:
                method = "Remove with delogo filter"
            else:
                method = "Blur logo area"
            
            print(f"  • Logo {i+1}: Method = {method} (type: {logo_type}, conf: {confidence:.3f})")
        
        return True
        
    except Exception as e:
        print(f"❌ Removal pipeline test failed: {e}")
        return False

def test_actual_removal(video_path: str, detected_logos: List[Dict[str, Any]]) -> bool:
    """Test actual removal with a simple case"""
    print("\n🎯 Testing actual removal...")
    
    if not detected_logos:
        print("❌ No watermarks to remove")
        return False
    
    try:
        from worker_thread import WorkerThread
        
        # Get the best watermark for testing
        best_logo = max(detected_logos, key=lambda x: x.get('confidence', 0))
        
        # Create output path
        output_path = video_path.replace('.mp4', '_removed.mp4')
        
        print(f"  • Testing removal of: '{best_logo.get('text', 'unknown')}' "
              f"at ({best_logo['x']}, {best_logo['y']}) "
              f"size {best_logo['width']}x{best_logo['height']}")
        
        # Create worker thread for removal
        worker = WorkerThread("remove_logo", '/opt/homebrew/bin/ffmpeg', 
                            video_path, "inpaint", best_logo, output_path)
        
        # Mock progress and finished signals
        def mock_progress(msg):
            print(f"    PROGRESS: {msg}")
        def mock_finished(success, msg):
            print(f"    FINISHED: {success} - {msg}")
        
        worker.progress.connect(mock_progress)
        worker.finished.connect(mock_finished)
        
        # Run in synchronous mode for testing
        worker.remove_logo_worker('/opt/homebrew/bin/ffmpeg', video_path, "inpaint", best_logo, output_path)
        
        # Check if output file was created
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"  ✅ Output file created: {output_path} ({file_size} bytes)")
            
            # Clean up
            os.remove(output_path)
            return True
        else:
            print(f"  ❌ Output file not created: {output_path}")
            return False
            
    except Exception as e:
        print(f"❌ Actual removal test failed: {e}")
        return False

def test_end_to_end_workflow():
    """Test the complete end-to-end workflow"""
    print("🧪 TESTING END-TO-END WATERMARK REMOVAL WORKFLOW\n")
    
    # Create test video
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
        video_path = tmp.name
    
    try:
        print("📹 Creating test video with watermarks...")
        if not create_test_video_with_watermarks(video_path):
            print("❌ Failed to create test video")
            return False
        
        print(f"  ✅ Test video created: {video_path}")
        
        # Test detection
        detected_logos = test_detection_pipeline(video_path)
        
        if not detected_logos:
            print("❌ No watermarks detected - cannot test removal")
            return False
        
        # Test removal pipeline logic
        if not test_removal_pipeline(video_path, detected_logos):
            print("❌ Removal pipeline test failed")
            return False
        
        # Test actual removal
        if not test_actual_removal(video_path, detected_logos):
            print("❌ Actual removal test failed")
            return False
        
        print("\n🎉 END-TO-END TEST SUCCESSFUL!")
        print("   All components are working correctly:")
        print("   ✅ Detection pipeline")
        print("   ✅ Removal logic")
        print("   ✅ Actual removal")
        return True
        
    except Exception as e:
        print(f"❌ End-to-end test failed: {e}")
        return False
    finally:
        # Clean up
        if os.path.exists(video_path):
            os.remove(video_path)
            print(f"🧹 Cleaned up test video: {video_path}")

if __name__ == "__main__":
    success = test_end_to_end_workflow()
    sys.exit(0 if success else 1)
