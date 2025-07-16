#!/usr/bin/env python3
"""
Quick test to verify the LogoDetector initialization fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_logo_detector_init():
    """Test LogoDetector initialization with ffmpeg_path"""
    
    print("🧪 Testing LogoDetector initialization fix...")
    
    try:
        from logo_detector import LogoDetector
        
        # Test with ffmpeg_path
        detector = LogoDetector('ffmpeg')
        print("✅ LogoDetector initialized successfully with ffmpeg_path")
        
        # Test video operations integration
        from video_operations import VideoOperations
        
        class MockWindow:
            def __init__(self):
                self.ffmpeg_path = 'ffmpeg'
                
            def log_message(self, msg):
                print(f"📝 {msg}")
                
            def show_error(self, msg):
                print(f"❌ {msg}")
                
            def start_operation(self, operation):
                print(f"🚀 {operation}")
                
            def finish_operation(self, success, msg):
                print(f"✅ {msg}")
        
        mock_window = MockWindow()
        video_ops = VideoOperations(mock_window)
        
        print("✅ VideoOperations initialized successfully")
        print(f"✅ ffmpeg_path accessible: {video_ops.ffmpeg_path}")
        
        # Test that the detector can be created in the video operations context
        test_detector = LogoDetector(video_ops.ffmpeg_path)
        print("✅ LogoDetector can be created with video_ops.ffmpeg_path")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_logo_detector_init()
    if success:
        print("\n🎉 LogoDetector initialization fix successful!")
        print("The automatic detection should now work properly.")
    else:
        print("\n❌ LogoDetector initialization fix failed!")
    
    sys.exit(0 if success else 1)
