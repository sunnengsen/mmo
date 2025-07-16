#!/usr/bin/env python3
"""
Debug script to check actual video dimensions and test coordinate validation
"""
import subprocess
import sys

def check_video_info(video_path):
    """Check the actual dimensions of the video causing the issue"""
    print(f"🔍 Analyzing video: {video_path}")
    
    # Get video information
    try:
        probe_cmd = [
            "ffprobe", "-v", "error", "-select_streams", "v:0", 
            "-show_entries", "stream=width,height", 
            "-of", "csv=p=0:s=x", video_path
        ]
        probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
        if probe_result.returncode == 0:
            dimensions = probe_result.stdout.strip()
            if 'x' in dimensions:
                width, height = map(int, dimensions.split('x'))
            else:
                # Fallback method
                width_cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width", "-of", "csv=p=0", video_path]
                height_cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=height", "-of", "csv=p=0", video_path]
                
                width_result = subprocess.run(width_cmd, capture_output=True, text=True)
                height_result = subprocess.run(height_cmd, capture_output=True, text=True)
                
                width = int(width_result.stdout.strip())
                height = int(height_result.stdout.strip())
            
            print(f"✅ Video dimensions: {width}x{height}")
            return width, height
        else:
            print(f"❌ Failed to get video info: {probe_result.stderr}")
            return None, None
    except Exception as e:
        print(f"❌ Error getting video info: {e}")
        return None, None

def test_delogo_coordinates(video_path, x, y, w, h):
    """Test if specific coordinates work with delogo filter"""
    print(f"\n🧪 Testing delogo coordinates: x={x}, y={y}, w={w}, h={h}")
    
    try:
        # Test with a very short duration to avoid creating large files
        cmd = [
            "ffmpeg", "-i", video_path,
            "-vf", f"delogo=x={x}:y={y}:w={w}:h={h}:show=0",
            "-t", "1", "-f", "null", "-"  # Output to null to test filter only
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Coordinates are valid")
            return True
        else:
            print(f"❌ Coordinates failed: {result.stderr}")
            if "Logo area is outside of the frame" in result.stderr:
                print("   - Error: Logo area is outside of the frame")
            return False
    except Exception as e:
        print(f"❌ Error testing coordinates: {e}")
        return False

def main():
    video_path = "/Users/sunnengsen/Desktop/part_000.mp4"
    
    # Check if video exists
    import os
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        print("Please update the video_path variable to point to your actual video file")
        return
    
    # Get actual video dimensions
    width, height = check_video_info(video_path)
    if width is None or height is None:
        print("Cannot proceed without video dimensions")
        return
    
    # Test the problematic coordinates from the error
    problematic_coords = (0, 11, 242, 110)
    x, y, w, h = problematic_coords
    
    print(f"\n📊 Coordinate Analysis:")
    print(f"   Video size: {width}x{height}")
    print(f"   Logo area: ({x}, {y}) to ({x+w}, {y+h})")
    print(f"   Right edge: {x+w} (video width: {width})")
    print(f"   Bottom edge: {y+h} (video height: {height})")
    
    # Check boundaries
    if x + w > width:
        print(f"❌ Width overflow: {x+w} > {width} (overflow: {x+w-width} pixels)")
    else:
        print(f"✅ Width within bounds ({width-x-w} pixels margin)")
    
    if y + h > height:
        print(f"❌ Height overflow: {y+h} > {height} (overflow: {y+h-height} pixels)")
    else:
        print(f"✅ Height within bounds ({height-y-h} pixels margin)")
    
    # Test the coordinates
    test_delogo_coordinates(video_path, x, y, w, h)
    
    # Suggest corrected coordinates if needed
    if x + w > width or y + h > height:
        corrected_x = max(0, min(x, width - w))
        corrected_y = max(0, min(y, height - h))
        corrected_w = min(w, width - corrected_x)
        corrected_h = min(h, height - corrected_y)
        
        print(f"\n💡 Suggested corrected coordinates:")
        print(f"   Original: x={x}, y={y}, w={w}, h={h}")
        print(f"   Corrected: x={corrected_x}, y={corrected_y}, w={corrected_w}, h={corrected_h}")
        
        test_delogo_coordinates(video_path, corrected_x, corrected_y, corrected_w, corrected_h)

if __name__ == "__main__":
    main()
