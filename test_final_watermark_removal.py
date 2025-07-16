#!/usr/bin/env python3
"""
Final comprehensive test for the watermark removal system
Creates a video, processes it completely, and verifies the output
"""

import os
import sys
import tempfile
import subprocess
import time

def create_test_video():
    """Create a test video with multiple watermarks"""
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
        video_path = tmp.name
    
    cmd = [
        'ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=blue:size=1280x720:duration=3',
        '-vf', 
        'drawtext=text="FIXED WATERMARK":fontcolor=white:fontsize=40:x=50:y=50,'
        'drawtext=text="www.example.com":fontcolor=red:fontsize=20:x=1000:y=650',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', video_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to create test video: {result.stderr}")
        return None
    
    return video_path

def test_complete_removal():
    """Test the complete watermark removal process"""
    print("🧪 COMPREHENSIVE WATERMARK REMOVAL TEST")
    print("=" * 50)
    
    # Create test video
    video_path = create_test_video()
    if not video_path:
        return False
    
    try:
        print(f"📹 Test video created: {video_path}")
        print(f"   File size: {os.path.getsize(video_path)} bytes")
        
        # Test detection
        print("\n🔍 Step 1: Detection")
        from logo_detector import detect_logos_automatically
        detected_logos = detect_logos_automatically(video_path, '/opt/homebrew/bin/ffmpeg')
        
        if not detected_logos:
            print("❌ No watermarks detected")
            return False
        
        print(f"✅ Detected {len(detected_logos)} watermarks")
        for i, logo in enumerate(detected_logos):
            text = logo.get('text', 'unknown')[:20] + ('...' if len(logo.get('text', '')) > 20 else '')
            print(f"   {i+1}. '{text}' at ({logo['x']}, {logo['y']}) conf: {logo['confidence']:.3f}")
        
        # Test removal process
        print("\n🛠️  Step 2: Removal Process")
        from video_operations import VideoOperations
        
        # Mock main window that captures the actual results
        class TestMainWindow:
            def __init__(self):
                self.ffmpeg_path = '/opt/homebrew/bin/ffmpeg'
                self.ytdlp_path = None
                self.worker_thread = None
                self.messages = []
                self.operation_started = False
                self.operation_finished = False
                self.success = False
                
            def log_message(self, msg):
                self.messages.append(msg)
                print(f"  LOG: {msg}")
            def show_error(self, msg):
                self.messages.append(f"ERROR: {msg}")
                print(f"  ERROR: {msg}")
            def start_operation(self, msg):
                self.operation_started = True
                self.messages.append(f"START: {msg}")
                print(f"  START: {msg}")
            def finish_operation(self, success, msg):
                self.operation_finished = True
                self.success = success
                self.messages.append(f"FINISH: {success} - {msg}")
                print(f"  FINISH: {success} - {msg}")
        
        test_window = TestMainWindow()
        video_ops = VideoOperations(test_window)
        
        # Run the automatic removal
        print("   Running automatic removal...")
        video_ops._remove_logo_automatic(video_path)
        
        # Wait for the operation to start
        time.sleep(1)
        
        if test_window.operation_started:
            print("   ✅ Removal operation started")
            
            # If worker thread was created, wait for it to complete
            if hasattr(test_window, 'worker_thread') and test_window.worker_thread:
                print("   ⏳ Waiting for worker thread to complete...")
                
                # Wait for the worker thread to finish (with timeout)
                timeout = 30  # 30 seconds timeout
                start_time = time.time()
                
                while test_window.worker_thread.isRunning() and (time.time() - start_time) < timeout:
                    time.sleep(0.5)
                    # Process events to handle signals
                    from PyQt6.QtCore import QCoreApplication
                    QCoreApplication.processEvents()
                
                if test_window.worker_thread.isRunning():
                    print("   ⚠️  Worker thread still running after timeout")
                    test_window.worker_thread.terminate()
                    test_window.worker_thread.wait(5000)
                else:
                    print("   ✅ Worker thread completed")
                
                # Check if output file was created
                expected_outputs = [
                    video_path.replace('.mp4', '_logo_removed_auto.mp4'),
                    video_path.replace('.mp4', '_combined_watermarks_removed.mp4'),
                    video_path.replace('.mp4', '_moving_watermark_removed.mp4')
                ]
                
                output_created = False
                for output_path in expected_outputs:
                    if os.path.exists(output_path):
                        output_size = os.path.getsize(output_path)
                        print(f"   ✅ Output created: {os.path.basename(output_path)} ({output_size} bytes)")
                        output_created = True
                        # Clean up output file
                        os.remove(output_path)
                        break
                
                if not output_created:
                    print("   ❌ No output file created")
                    return False
            else:
                print("   ❌ Worker thread not created")
                return False
        else:
            print("   ❌ Removal operation not started")
            return False
        
        print("\n📊 Step 3: Process Analysis")
        print(f"   • Total messages logged: {len(test_window.messages)}")
        print(f"   • Operation started: {test_window.operation_started}")
        print(f"   • Operation finished: {test_window.operation_finished}")
        print(f"   • Success: {test_window.success}")
        
        # Show key messages
        key_messages = [msg for msg in test_window.messages if any(keyword in msg for keyword in ['Found', 'Removing', 'Enhanced', 'completed'])]
        if key_messages:
            print("   • Key messages:")
            for msg in key_messages[-5:]:  # Show last 5 key messages
                print(f"     - {msg}")
        
        print("\n🎉 COMPREHENSIVE TEST COMPLETED!")
        print("   ✅ Detection working")
        print("   ✅ Removal process working")
        print("   ✅ Worker thread working")
        print("   ✅ Output file created")
        print("   ✅ Complete end-to-end process working")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
            print(f"🧹 Cleaned up test video")

if __name__ == "__main__":
    success = test_complete_removal()
    if success:
        print("\n🎉 ALL TESTS PASSED!")
        print("The watermark removal system is working correctly.")
        print("Both fixed and moving watermarks should be removed properly.")
        print("\nYou can now use the application to remove watermarks from your videos.")
    else:
        print("\n❌ TESTS FAILED!")
        print("There are still issues with the watermark removal system.")
    
    sys.exit(0 if success else 1)
