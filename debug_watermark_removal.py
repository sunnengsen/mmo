#!/usr/bin/env python3
"""
Debug watermark removal issue
This script will help diagnose why watermark removal isn't working for fixed and moving positions
"""

import os
import sys
import tempfile
import subprocess
import cv2
import numpy as np

def create_debug_video():
    """Create a video with both fixed and moving watermarks for debugging"""
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
        video_path = tmp.name
    
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

def debug_detection(video_path):
    """Debug the detection process"""
    print(f"\n🔍 DEBUGGING DETECTION FOR: {video_path}")
    
    try:
        from logo_detector import detect_logos_automatically
        detected_logos = detect_logos_automatically(video_path, '/opt/homebrew/bin/ffmpeg')
        
        print(f"✅ Detection found {len(detected_logos)} watermarks")
        
        for i, logo in enumerate(detected_logos):
            print(f"\n📊 WATERMARK {i+1} DETAILS:")
            print(f"  • Text: '{logo.get('text', 'N/A')}'")
            print(f"  • Position: ({logo['x']}, {logo['y']}) {logo['width']}x{logo['height']}")
            print(f"  • Confidence: {logo.get('confidence', 0):.3f}")
            print(f"  • Type: {logo.get('type', 'unknown')}")
            print(f"  • Corner: {logo.get('corner', 'unknown')}")
            print(f"  • Is watermark: {logo.get('is_watermark', False)}")
            print(f"  • Multi-frame: {logo.get('multi_frame', False)}")
            print(f"  • Moving scan: {logo.get('moving_scan', False)}")
            print(f"  • Frame: {logo.get('frame', 'N/A')}")
            print(f"  • Timestamp: {logo.get('timestamp', 'N/A')}")
        
        return detected_logos
        
    except Exception as e:
        print(f"❌ Detection failed: {e}")
        import traceback
        traceback.print_exc()
        return []

def debug_removal_logic(detected_logos):
    """Debug the removal logic without actually removing"""
    print(f"\n🛠️  DEBUGGING REMOVAL LOGIC")
    
    if not detected_logos:
        print("❌ No watermarks to process")
        return
    
    try:
        from video_operations import VideoOperations
        
        # Mock main window for testing
        class MockMainWindow:
            def __init__(self):
                self.ffmpeg_path = '/opt/homebrew/bin/ffmpeg'
                self.ytdlp_path = None
                self.worker_thread = None
                
            def log_message(self, msg):
                print(f"    LOG: {msg}")
            def show_error(self, msg):
                print(f"    ERROR: {msg}")
            def start_operation(self, msg):
                print(f"    START: {msg}")
            def finish_operation(self, success, msg):
                print(f"    FINISH: {success} - {msg}")
        
        mock_window = MockMainWindow()
        video_ops = VideoOperations(mock_window)
        
        # Test grouping
        print(f"\n📋 GROUPING ANALYSIS:")
        watermark_groups = video_ops._group_watermarks_by_position(detected_logos)
        print(f"  • Input watermarks: {len(detected_logos)}")
        print(f"  • Grouped into: {len(watermark_groups)} groups")
        
        for i, group in enumerate(watermark_groups):
            print(f"  • Group {i+1}: {len(group)} watermarks")
            for j, watermark in enumerate(group):
                print(f"    - Watermark {j+1}: '{watermark.get('text', 'N/A')}' at ({watermark['x']}, {watermark['y']})")
        
        # Test moving watermark detection
        print(f"\n🎬 MOVING WATERMARK ANALYSIS:")
        has_moving = any(d.get('multi_frame', False) or d.get('moving_scan', False) for d in detected_logos)
        print(f"  • Has moving watermarks: {has_moving}")
        
        moving_watermarks = [d for d in detected_logos if d.get('multi_frame', False) or d.get('moving_scan', False)]
        static_watermarks = [d for d in detected_logos if not (d.get('multi_frame', False) or d.get('moving_scan', False))]
        
        print(f"  • Moving watermarks: {len(moving_watermarks)}")
        print(f"  • Static watermarks: {len(static_watermarks)}")
        
        # Test removal path decision
        print(f"\n🎯 REMOVAL PATH DECISION:")
        if has_moving:
            print("  • Would use: _remove_moving_watermarks()")
            if len(watermark_groups) == 1:
                print("    → Single moving watermark path")
            else:
                print("    → Multiple watermarks path")
        else:
            print("  • Would use: _remove_single_watermark()")
        
        # Test method selection for each watermark
        print(f"\n⚙️  METHOD SELECTION:")
        for i, logo in enumerate(detected_logos):
            logo_type = logo.get('type', 'unknown')
            confidence = logo.get('confidence', 0)
            is_watermark = logo.get('is_watermark', False)
            
            if 'ocr_' in logo_type or is_watermark:
                method = "Smart inpaint (recommended for text)"
                reason = f"OCR detected or watermark flag (type: {logo_type}, watermark: {is_watermark})"
            elif 'text' in logo_type or 'website' in logo_type:
                method = "Smart inpaint (recommended for text)"
                reason = f"Text content detected (type: {logo_type})"
            elif confidence > 0.7:
                method = "Remove with delogo filter"
                reason = f"High confidence (conf: {confidence:.3f})"
            else:
                method = "Blur logo area"
                reason = f"Standard detection (conf: {confidence:.3f})"
            
            print(f"  • Watermark {i+1}: {method}")
            print(f"    Reason: {reason}")
        
        return True
        
    except Exception as e:
        print(f"❌ Removal logic debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def debug_worker_thread_logic(detected_logos):
    """Debug the worker thread logic"""
    print(f"\n🔧 DEBUGGING WORKER THREAD LOGIC")
    
    if not detected_logos:
        print("❌ No watermarks to process")
        return
    
    try:
        from worker_thread import WorkerThread
        
        # Test the logo removal command generation
        best_logo = max(detected_logos, key=lambda x: x.get('confidence', 0))
        
        print(f"📝 COMMAND GENERATION TEST:")
        print(f"  • Selected logo: '{best_logo.get('text', 'N/A')}'")
        print(f"  • Position: ({best_logo['x']}, {best_logo['y']}) {best_logo['width']}x{best_logo['height']}")
        print(f"  • Method: inpaint")
        
        # Simulate the padding logic
        x, y, w, h = best_logo['x'], best_logo['y'], best_logo['width'], best_logo['height']
        padding = 5
        x_padded = max(0, x - padding)
        y_padded = max(0, y - padding)
        w_padded = w + (2 * padding)
        h_padded = h + (2 * padding)
        
        print(f"  • Original area: ({x}, {y}) {w}x{h}")
        print(f"  • Padded area: ({x_padded}, {y_padded}) {w_padded}x{h_padded}")
        
        # Generate the filter command
        if best_logo.get('type') == 'moving_watermark':
            filter_complex = f"[0:v]crop={w_padded}:{h_padded}:{x_padded}:{y_padded},median=7,gblur=sigma=2[cleaned];[0:v][cleaned]overlay={x_padded}:{y_padded}[out]"
        else:
            filter_complex = f"[0:v]crop={w_padded}:{h_padded}:{x_padded}:{y_padded},median=5[cleaned];[0:v][cleaned]overlay={x_padded}:{y_padded}[out]"
        
        print(f"  • Filter command: {filter_complex}")
        
        return True
        
    except Exception as e:
        print(f"❌ Worker thread logic debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main debug function"""
    print("🐛 WATERMARK REMOVAL DEBUG TOOL")
    print("=" * 50)
    
    # Create test video
    print("📹 Creating test video...")
    video_path = create_debug_video()
    if not video_path:
        print("❌ Failed to create test video")
        return
    
    print(f"✅ Test video created: {video_path}")
    
    try:
        # Debug detection
        detected_logos = debug_detection(video_path)
        
        if not detected_logos:
            print("❌ No watermarks detected - cannot debug removal")
            return
        
        # Debug removal logic
        if not debug_removal_logic(detected_logos):
            print("❌ Removal logic debug failed")
            return
        
        # Debug worker thread
        if not debug_worker_thread_logic(detected_logos):
            print("❌ Worker thread debug failed")
            return
        
        print("\n🎉 DEBUG COMPLETED SUCCESSFULLY!")
        print("   All components appear to be working correctly.")
        print("   If removal is still not working, the issue might be:")
        print("   1. Video format/codec compatibility")
        print("   2. FFmpeg filter execution")
        print("   3. UI integration issues")
        
    finally:
        # Clean up
        if os.path.exists(video_path):
            os.remove(video_path)
            print(f"🧹 Cleaned up test video: {video_path}")

if __name__ == "__main__":
    main()
