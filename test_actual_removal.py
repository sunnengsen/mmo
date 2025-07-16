#!/usr/bin/env python3
"""
Test actual watermark removal with real FFmpeg processing
"""

import os
import sys
import tempfile
import subprocess
import time

def create_test_video_with_visible_watermark():
    """Create a test video with a clearly visible watermark"""
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
        video_path = tmp.name
    
    # Create a video with a very obvious watermark
    cmd = [
        'ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=blue:size=1280x720:duration=5',
        '-vf', 
        'drawtext=text="WATERMARK":fontcolor=white:fontsize=60:x=100:y=100:box=1:boxcolor=black@0.5',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', video_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to create test video: {result.stderr}")
        return None
    
    print(f"✅ Created test video: {video_path}")
    return video_path

def test_ffmpeg_removal_directly():
    """Test FFmpeg removal commands directly"""
    print("🧪 TESTING FFMPEG REMOVAL DIRECTLY")
    print("=" * 50)
    
    # Create test video
    input_video = create_test_video_with_visible_watermark()
    if not input_video:
        return False
    
    try:
        output_video = input_video.replace('.mp4', '_removed.mp4')
        
        # Test the exact filter we're using
        x, y, w, h = 95, 95, 110, 70  # Covering the WATERMARK text
        
        print(f"🎯 Testing removal area: ({x}, {y}) {w}x{h}")
        
        # Test different removal methods
        methods = [
            ("blur", f"[0:v]crop={w}:{h}:{x}:{y},gblur=sigma=15[blurred];[0:v][blurred]overlay={x}:{y}[out]"),
            ("inpaint", f"[0:v]crop={w}:{h}:{x}:{y},median=5[cleaned];[0:v][cleaned]overlay={x}:{y}[out]"),
            ("delogo", f"delogo=x={x}:y={y}:w={w}:h={h}:show=0"),
            ("blackout", f"drawbox=x={x}:y={y}:w={w}:h={h}:color=black@0.8:t=fill")
        ]
        
        for method_name, filter_cmd in methods:
            output_path = input_video.replace('.mp4', f'_removed_{method_name}.mp4')
            
            print(f"\n🔧 Testing {method_name} method...")
            print(f"   Filter: {filter_cmd}")
            
            if "filter_complex" in filter_cmd or "[" in filter_cmd:
                # Complex filter
                cmd = [
                    'ffmpeg', '-y', '-i', input_video,
                    '-filter_complex', filter_cmd,
                    '-map', '[out]', '-map', '0:a?',
                    '-c:v', 'libx264', '-crf', '23', '-preset', 'fast',
                    output_path
                ]
            else:
                # Simple filter
                cmd = [
                    'ffmpeg', '-y', '-i', input_video,
                    '-vf', filter_cmd,
                    '-c:v', 'libx264', '-crf', '23', '-preset', 'fast',
                    output_path
                ]
            
            print(f"   Command: {' '.join(cmd[-10:])}")  # Show last 10 parts
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                if os.path.exists(output_path):
                    size = os.path.getsize(output_path)
                    print(f"   ✅ SUCCESS: Output created ({size} bytes)")
                    
                    # Check if the file is actually different
                    input_size = os.path.getsize(input_video)
                    if abs(size - input_size) > 1000:  # More than 1KB difference
                        print(f"   📊 File size changed: {input_size} → {size}")
                    else:
                        print(f"   ⚠️  File size similar: {input_size} → {size}")
                    
                    os.remove(output_path)  # Clean up
                else:
                    print(f"   ❌ FAILED: Output file not created")
            else:
                print(f"   ❌ FAILED: FFmpeg error")
                print(f"   Error: {result.stderr[:200]}...")
        
        return True
        
    finally:
        if os.path.exists(input_video):
            os.remove(input_video)
            print(f"\n🧹 Cleaned up test video")

def test_system_integration():
    """Test the complete system integration"""
    print("\n🔗 TESTING SYSTEM INTEGRATION")
    print("=" * 50)
    
    # Create test video
    input_video = create_test_video_with_visible_watermark()
    if not input_video:
        return False
    
    try:
        # Test detection
        print("🔍 Step 1: Detection")
        from logo_detector import detect_logos_automatically
        
        detected_logos = detect_logos_automatically(input_video, '/opt/homebrew/bin/ffmpeg')
        
        if not detected_logos:
            print("❌ No watermarks detected")
            return False
        
        print(f"✅ Detected {len(detected_logos)} watermarks:")
        for i, logo in enumerate(detected_logos):
            print(f"   {i+1}. '{logo.get('text', 'N/A')}' at ({logo['x']}, {logo['y']}) {logo['width']}x{logo['height']}")
        
        # Test removal using our system
        print("\n🛠️  Step 2: System Removal")
        from video_operations import VideoOperations
        from worker_thread import WorkerThread
        
        # Select the best watermark
        best_logo = max(detected_logos, key=lambda x: x.get('confidence', 0))
        output_path = input_video.replace('.mp4', '_system_removed.mp4')
        
        print(f"🎯 Removing watermark: '{best_logo.get('text', 'N/A')}'")
        print(f"   Position: ({best_logo['x']}, {best_logo['y']}) {best_logo['width']}x{best_logo['height']}")
        
        # Create worker thread and run removal
        worker = WorkerThread("remove_logo", '/opt/homebrew/bin/ffmpeg', 
                            input_video, "inpaint", best_logo, output_path)
        
        # Mock the signals
        def progress_handler(msg):
            print(f"   PROGRESS: {msg}")
        
        def finished_handler(success, msg):
            print(f"   FINISHED: {success} - {msg}")
        
        worker.progress.connect(progress_handler)
        worker.finished.connect(finished_handler)
        
        # Run the worker (synchronously for testing)
        print("   Running worker thread...")
        worker.remove_logo_worker('/opt/homebrew/bin/ffmpeg', input_video, "inpaint", best_logo, output_path)
        
        # Check result
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"   ✅ System removal successful ({size} bytes)")
            os.remove(output_path)
            return True
        else:
            print(f"   ❌ System removal failed - no output file")
            return False
        
    finally:
        if os.path.exists(input_video):
            os.remove(input_video)

def main():
    print("🔧 WATERMARK REMOVAL DIAGNOSTIC TOOL")
    print("=" * 60)
    
    # Test FFmpeg directly
    success1 = test_ffmpeg_removal_directly()
    
    # Test system integration
    success2 = test_system_integration()
    
    print(f"\n📊 DIAGNOSTIC RESULTS:")
    print(f"   FFmpeg Direct Test: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"   System Integration: {'✅ PASS' if success2 else '❌ FAIL'}")
    
    if success1 and success2:
        print(f"\n🎉 DIAGNOSIS: System is working correctly!")
        print(f"   If watermarks are still visible, the issue might be:")
        print(f"   1. Detection coordinates are incorrect")
        print(f"   2. Watermark area is too large or complex")
        print(f"   3. Video encoding settings")
        print(f"   4. Watermark blends with background")
    else:
        print(f"\n❌ DIAGNOSIS: System has issues!")
        print(f"   Check FFmpeg installation and filter compatibility")

if __name__ == "__main__":
    main()
