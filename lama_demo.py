#!/usr/bin/env python3
"""
Lama-Cleaner Demo for Watermark Removal
This script demonstrates how to use lama-cleaner with your existing watermark detection system
"""

import os
import sys
import cv2
import numpy as np
import shutil
from pathlib import Path

def check_lama_cleaner():
    """Check if lama-cleaner is properly installed"""
    try:
        import subprocess
        result = subprocess.run(['lama-cleaner', '--help'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def create_test_video_with_watermark():
    """Create a simple test video with a watermark for demonstration"""
    print("🎬 Creating test video with watermark...")
    
    # Video properties
    width, height = 640, 480
    fps = 30
    duration = 5  # seconds
    total_frames = fps * duration
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_path = 'test_video_with_watermark.mp4'
    out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
    
    for frame_num in range(total_frames):
        # Create frame with moving content
        frame = np.ones((height, width, 3), dtype=np.uint8) * 200  # Light gray
        
        # Add moving circle (main content)
        circle_x = int(50 + (width - 100) * frame_num / total_frames)
        circle_y = height // 2
        cv2.circle(frame, (circle_x, circle_y), 30, (100, 150, 200), -1)
        
        # Add static watermark
        watermark_x, watermark_y = width - 150, 30
        cv2.rectangle(frame, (watermark_x, watermark_y), (watermark_x + 120, watermark_y + 40), (50, 50, 50), -1)
        cv2.putText(frame, "WATERMARK", (watermark_x + 5, watermark_y + 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Add frame number
        cv2.putText(frame, f"Frame {frame_num + 1}/{total_frames}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        
        out.write(frame)
    
    out.release()
    print(f"✅ Created test video: {video_path}")
    return video_path

def demo_image_watermark_removal():
    """Demonstrate watermark removal on a single image"""
    print("\n🖼️  DEMO 1: Single Image Watermark Removal")
    print("=" * 50)
    
    # Create test image with watermark
    image = np.ones((400, 600, 3), dtype=np.uint8) * 240
    
    # Add content
    cv2.rectangle(image, (50, 50), (550, 150), (100, 150, 200), -1)
    cv2.putText(image, "Original Content", (200, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Add watermark
    cv2.rectangle(image, (400, 250), (580, 320), (50, 50, 50), -1)
    cv2.putText(image, "WATERMARK", (410, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Create mask
    mask = np.zeros((400, 600), dtype=np.uint8)
    cv2.rectangle(mask, (395, 245), (585, 325), 255, -1)  # Slightly larger than watermark
    
    # Save files
    input_path = "demo_input.png"
    mask_path = "demo_mask.png"
    output_path = "demo_output.png"
    
    cv2.imwrite(input_path, image)
    cv2.imwrite(mask_path, mask)
    
    print(f"📁 Input image: {input_path}")
    print(f"📁 Mask image: {mask_path}")
    
    # Use lama-cleaner
    try:
        from lama_integration import LamaCleaner
        
        with LamaCleaner(model_name="lama") as cleaner:
            success = cleaner.remove_watermark_from_image(input_path, mask_path, output_path)
            
        if success:
            print(f"✅ Success! Cleaned image: {output_path}")
            print("💡 Compare the before/after images to see the watermark removal!")
        else:
            print("❌ Watermark removal failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure lama-cleaner is installed: pip install lama-cleaner")

def demo_video_watermark_removal():
    """Demonstrate watermark removal on a video using existing detection system"""
    print("\n🎬 DEMO 2: Video Watermark Removal with Auto-Detection")
    print("=" * 50)
    
    # Create test video
    video_path = create_test_video_with_watermark()
    
    try:
        # Import your existing detection system
        from logo_detector import LogoDetector
        from lama_integration import LamaCleaner
        
        # Detect watermarks
        print("🔍 Detecting watermarks in video...")
        detector = LogoDetector("ffmpeg")  # Assumes ffmpeg is in PATH
        
        # Extract a frame for analysis
        frame = detector.extract_frame(video_path, 2.0)
        if frame is None:
            print("❌ Could not extract frame from video")
            return
            
        # Detect logos in the frame
        detections = detector.detect_logos_in_corners(frame)
        
        if not detections:
            print("⚠️  No watermarks detected automatically")
            print("💡 Try creating a more obvious watermark or use manual detection")
            return
            
        print(f"✅ Found {len(detections)} watermark(s)")
        
        # Show detection info
        for i, detection in enumerate(detections):
            print(f"  {i+1}. Position: ({detection['x']}, {detection['y']}) "
                  f"Size: {detection['width']}x{detection['height']} "
                  f"Confidence: {detection['confidence']:.2f}")
            if 'text' in detection:
                print(f"     Text: '{detection['text']}'")
        
        # For demo, we'll just remove watermarks from individual frames
        # Full video processing would require more time and resources
        print("\n🎨 Applying lama-cleaner to remove watermarks...")
        
        # Extract a few frames and process them
        output_dir = "demo_frames_processed"
        os.makedirs(output_dir, exist_ok=True)
        
        with LamaCleaner(model_name="lama") as cleaner:
            # Process frames 60, 90, 120 (2, 3, 4 seconds)
            for frame_time in [2.0, 3.0, 4.0]:
                frame = detector.extract_frame(video_path, frame_time)
                if frame is None:
                    continue
                    
                # Create mask from detections
                mask = cleaner.create_mask_from_detections(frame.shape, detections)
                
                # Save frame and mask
                frame_path = os.path.join(output_dir, f"frame_{frame_time:.1f}s.png")
                mask_path = os.path.join(output_dir, f"mask_{frame_time:.1f}s.png")
                output_path = os.path.join(output_dir, f"cleaned_{frame_time:.1f}s.png")
                
                cv2.imwrite(frame_path, frame)
                cv2.imwrite(mask_path, mask)
                
                # Apply lama-cleaner
                success = cleaner.remove_watermark_from_image(frame_path, mask_path, output_path)
                
                if success:
                    print(f"✅ Processed frame at {frame_time}s")
                else:
                    print(f"❌ Failed to process frame at {frame_time}s")
        
        print(f"\n📁 Processed frames saved in: {output_dir}/")
        print("💡 Compare the original frames with cleaned versions!")
        
    except ImportError as e:
        print(f"❌ Missing required modules: {e}")
        print("💡 Make sure you have: pip install opencv-python")
    except Exception as e:
        print(f"❌ Error during video processing: {e}")

def demo_integration_with_existing_system():
    """Show how to integrate lama-cleaner with existing video operations"""
    print("\n🔧 DEMO 3: Integration with Existing System")
    print("=" * 50)
    
    print("To integrate lama-cleaner into your existing video operations:")
    print()
    print("1. 📂 The system already has:")
    print("   ✅ logo_detector.py - Automatic watermark detection")
    print("   ✅ video_operations.py - Video processing operations")
    print("   ✅ lama_integration.py - Lama-cleaner integration")
    print()
    print("2. 🛠️  To add lama-cleaner as a removal option:")
    print("   • Update video_operations.py to include 'Lama Inpainting' method")
    print("   • Add UI button for advanced watermark removal")
    print("   • Integrate with existing detection pipeline")
    print()
    print("3. 🎯 Lama-cleaner is best for:")
    print("   • Complex watermarks with text")
    print("   • Watermarks over detailed backgrounds")  
    print("   • High-quality inpainting results")
    print()
    print("4. ⚡ Current methods vs Lama-cleaner:")
    print("   • Blur: Fast, good for simple logos")
    print("   • Delogo: Fast, good for solid color logos")
    print("   • Lama: Slower, best quality for complex watermarks")

def main():
    """Main demo function"""
    print("🎨 LAMA-CLEANER WATERMARK REMOVAL DEMO")
    print("=" * 60)
    
    # Check if lama-cleaner is installed
    if not check_lama_cleaner():
        print("❌ lama-cleaner not found!")
        print("📦 Install it with: pip install lama-cleaner")
        print("💡 After installation, run this demo again")
        return
    
    print("✅ lama-cleaner is installed and ready!")
    print()
    
    # Run demos
    demo_image_watermark_removal()
    demo_video_watermark_removal()
    demo_integration_with_existing_system()
    
    print("\n🎉 DEMO COMPLETE!")
    print("=" * 60)
    print("💡 Next steps:")
    print("1. Try the demos on your own images/videos")
    print("2. Integrate lama-cleaner into your video operations")
    print("3. Experiment with different models (lama, ldm, zits, etc.)")
    print("\n📚 More info: https://github.com/Sanster/lama-cleaner")

if __name__ == "__main__":
    main()
