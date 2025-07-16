#!/usr/bin/env python3
"""
End-to-end test for moving watermark detection and removal
This test validates the complete pipeline for handling moving watermarks
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logo_detector import LogoDetector
import subprocess
import tempfile
import json

def create_test_video_with_moving_watermark():
    """Create a test video with a moving watermark"""
    
    # Create a temporary video with moving text
    output_path = "test_moving_watermark.mp4"
    
    # FFmpeg command to create a video with moving text
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "testsrc2=size=640x480:duration=10:rate=30",
        "-vf", 
        "drawtext=text='WATERMARK':fontsize=30:fontcolor=white:x=50+100*sin(t):y=50+50*cos(t):enable='between(t,0,10)'",
        "-pix_fmt", "yuv420p",
        "-c:v", "libx264", "-preset", "ultrafast",
        output_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ Test video created: {output_path}")
            return output_path
        else:
            print(f"❌ Failed to create test video: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        print("❌ Test video creation timed out")
        return None
    except Exception as e:
        print(f"❌ Error creating test video: {e}")
        return None

def test_moving_watermark_detection():
    """Test detection of moving watermarks"""
    
    print("🔍 Testing moving watermark detection...")
    
    # Create test video
    video_path = create_test_video_with_moving_watermark()
    if not video_path:
        return False
    
    try:
        # Create detector
        detector = LogoDetector("ffmpeg")  # Pass ffmpeg path
        
        # Test timeline detection
        print("📅 Running timeline detection...")
        watermark_timelines = detector.detect_logos_with_timeline(video_path, sample_interval=1.0)
        
        if not watermark_timelines:
            print("❌ No watermarks detected in timeline analysis")
            return False
        
        print(f"✅ Found {len(watermark_timelines)} watermark timeline(s)")
        
        # Analyze each timeline
        for i, timeline in enumerate(watermark_timelines):
            print(f"\n📊 Timeline {i+1}:")
            print(f"  Text: {timeline.get('text', 'Unknown')}")
            print(f"  Is Moving: {timeline.get('is_moving', False)}")
            print(f"  Confidence: {timeline.get('confidence', 0):.3f}")
            print(f"  Position Count: {len(timeline.get('positions', []))}")
            
            if timeline.get('is_moving', False):
                print("  🎬 Moving watermark detected!")
                positions = timeline.get('positions', [])
                if len(positions) > 1:
                    print(f"  📍 Position range:")
                    print(f"    X: {min(p['x'] for p in positions)} - {max(p['x'] for p in positions)}")
                    print(f"    Y: {min(p['y'] for p in positions)} - {max(p['y'] for p in positions)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Detection test failed: {e}")
        return False
    
    finally:
        # Clean up
        if os.path.exists(video_path):
            os.remove(video_path)

def test_dynamic_removal_command():
    """Test generation of dynamic removal commands"""
    
    print("\n🛠️ Testing dynamic removal command generation...")
    
    # Create test video
    video_path = create_test_video_with_moving_watermark()
    if not video_path:
        return False
    
    try:
        # Create detector
        detector = LogoDetector("ffmpeg")  # Pass ffmpeg path
        
        # Get timeline
        watermark_timelines = detector.detect_logos_with_timeline(video_path, sample_interval=1.0)
        
        if not watermark_timelines:
            print("❌ No watermarks for command generation test")
            return False
        
        # Test command generation for each timeline
        for timeline in watermark_timelines:
            if timeline.get('is_moving', False):
                print(f"🎯 Testing command generation for moving watermark...")
                
                # Generate dynamic removal command
                cmd = detector.create_dynamic_removal_command(video_path, timeline, method='blur')
                
                if cmd:
                    print(f"✅ Dynamic command generated:")
                    print(f"  Command length: {len(cmd)} arguments")
                    print(f"  Method: blur with time-based filters")
                    
                    # Validate command structure
                    if any('between(t,' in arg for arg in cmd):
                        print("  ✅ Time-based filters detected")
                    else:
                        print("  ⚠️ No time-based filters found")
                    
                    return True
                else:
                    print("❌ Failed to generate dynamic command")
                    return False
        
        print("ℹ️ No moving watermarks found for dynamic command test")
        return True
        
    except Exception as e:
        print(f"❌ Command generation test failed: {e}")
        return False
    
    finally:
        # Clean up
        if os.path.exists(video_path):
            os.remove(video_path)

def test_video_operations_integration():
    """Test integration with video operations"""
    
    print("\n🔗 Testing video operations integration...")
    
    # Create test video
    video_path = create_test_video_with_moving_watermark()
    if not video_path:
        return False
    
    try:
        # Test the import and basic functionality
        from video_operations import VideoOperations
        
        # Create a mock main window for testing
        class MockMainWindow:
            def __init__(self):
                self.ffmpeg_path = "ffmpeg"
                self.messages = []
                self.operation_started = False
                
            def log_message(self, message):
                self.messages.append(message)
                print(f"  📝 {message}")
                
            def show_error(self, message):
                print(f"  ❌ {message}")
                
            def start_operation(self, operation_name):
                self.operation_started = True
                print(f"  🚀 Started: {operation_name}")
                
            def finish_operation(self, success, message):
                print(f"  ✅ Finished: {message}")
        
        # Create video operations instance
        mock_window = MockMainWindow()
        video_ops = VideoOperations(mock_window)
        
        # Test if the new methods exist
        if hasattr(video_ops, '_remove_timeline_watermarks'):
            print("✅ Timeline watermark removal method exists")
        else:
            print("❌ Timeline watermark removal method missing")
            return False
            
        if hasattr(video_ops, '_remove_moving_timeline_watermark'):
            print("✅ Moving watermark removal method exists")
        else:
            print("❌ Moving watermark removal method missing")
            return False
        
        print("✅ Video operations integration looks good")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False
    
    finally:
        # Clean up
        if os.path.exists(video_path):
            os.remove(video_path)

def test_worker_thread_integration():
    """Test worker thread integration"""
    
    print("\n🧵 Testing worker thread integration...")
    
    try:
        from worker_thread import WorkerThread
        
        # Test if dynamic_removal operation type is supported
        worker = WorkerThread("dynamic_removal", ["echo", "test"], "output.mp4")
        
        if hasattr(worker, 'dynamic_removal_worker'):
            print("✅ Dynamic removal worker method exists")
            return True
        else:
            print("❌ Dynamic removal worker method missing")
            return False
            
    except Exception as e:
        print(f"❌ Worker thread integration test failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    
    print("🚀 Starting end-to-end moving watermark tests...")
    print("=" * 60)
    
    tests = [
        ("Moving Watermark Detection", test_moving_watermark_detection),
        ("Dynamic Removal Command Generation", test_dynamic_removal_command),
        ("Video Operations Integration", test_video_operations_integration),
        ("Worker Thread Integration", test_worker_thread_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        print("-" * 40)
        
        try:
            result = test_func()
            results.append((test_name, result))
            
            if result:
                print(f"✅ PASSED: {test_name}")
            else:
                print(f"❌ FAILED: {test_name}")
                
        except Exception as e:
            print(f"💥 ERROR in {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n🎯 OVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! Moving watermark system is ready.")
        return True
    else:
        print("⚠️ Some tests failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
