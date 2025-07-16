#!/usr/bin/env python3
"""
Test the exact user workflow for watermark removal
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from video_operations import VideoOperations
    from worker_thread import WorkerThread
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

class TestMainWindow:
    """Mock main window for testing"""
    
    def __init__(self):
        self.ffmpeg_path = "ffmpeg"
        self.worker_thread = None
        self.operation_active = False
    
    def log_message(self, message):
        print(f"LOG: {message}")
    
    def show_error(self, message):
        print(f"ERROR: {message}")
    
    def start_operation(self, operation_name):
        print(f"START: {operation_name}")
        self.operation_active = True
    
    def finish_operation(self, success, message):
        print(f"FINISH: {'Success' if success else 'Failed'} - {message}")
        self.operation_active = False

def test_automatic_removal():
    """Test the automatic watermark removal process"""
    
    print("🧪 Testing Automatic Watermark Removal")
    print("=" * 50)
    
    # Check if test video exists
    test_video = "test_simple_watermark.mp4"
    if not os.path.exists(test_video):
        print(f"❌ Test video {test_video} not found!")
        return False
    
    # Create mock main window
    main_window = TestMainWindow()
    
    # Create video operations
    video_ops = VideoOperations(main_window)
    
    # Test the automatic removal process
    print(f"📹 Testing automatic removal on: {test_video}")
    
    try:
        # This should trigger the entire automatic removal pipeline
        video_ops._remove_logo_automatic(test_video)
        
        print("✅ Automatic removal process initiated")
        
        # Wait a bit for any background processing
        import time
        time.sleep(2)
        
        return True
        
    except Exception as e:
        print(f"❌ Automatic removal failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_manual_removal():
    """Test manual watermark removal with known coordinates"""
    
    print("\n🎯 Testing Manual Watermark Removal")
    print("=" * 50)
    
    # Create mock main window
    main_window = TestMainWindow()
    
    # Create video operations
    video_ops = VideoOperations(main_window)
    
    # Manual coordinates (validated)
    logo_position = {
        'x': 448,
        'y': 336, 
        'width': 191,
        'height': 143
    }
    
    print(f"🎯 Testing manual removal with coordinates: {logo_position}")
    
    try:
        # Test manual removal with delogo method
        method_type = "delogo"
        output_path = "test_simple_watermark_manual_removed.mp4"
        
        print(f"📁 Output will be saved to: {output_path}")
        
        # Create and test worker thread directly
        worker = WorkerThread("remove_logo", main_window.ffmpeg_path, 
                            "test_simple_watermark.mp4", method_type, 
                            logo_position, output_path)
        
        print("✅ Worker thread created")
        
        # Run the worker in the main thread for testing
        worker.remove_logo_worker(main_window.ffmpeg_path, "test_simple_watermark.mp4", 
                                method_type, logo_position, output_path)
        
        # Check if output file was created
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"✅ Manual removal successful: {output_path} ({size} bytes)")
            return True
        else:
            print(f"❌ Output file not created: {output_path}")
            return False
            
    except Exception as e:
        print(f"❌ Manual removal failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Watermark Removal Tests")
    print("=" * 60)
    
    # Test 1: Manual removal (more direct)
    manual_success = test_manual_removal()
    
    # Test 2: Automatic removal (full pipeline)
    auto_success = test_automatic_removal()
    
    print("\n📊 Test Results Summary")
    print("=" * 60)
    print(f"Manual Removal:    {'✅ SUCCESS' if manual_success else '❌ FAILED'}")
    print(f"Automatic Removal: {'✅ SUCCESS' if auto_success else '❌ FAILED'}")
    
    if manual_success and auto_success:
        print("\n🎉 All tests passed! Watermark removal is working.")
    elif manual_success:
        print("\n⚠️ Manual removal works, but automatic detection has issues.")
    else:
        print("\n❌ Watermark removal system has problems.")
    
    sys.exit(0 if (manual_success and auto_success) else 1)
