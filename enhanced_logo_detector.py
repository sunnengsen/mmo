#!/usr/bin/env python3
"""
Enhanced Logo Detector with Lama-Cleaner Integration
Combines existing FFmpeg-based removal with AI-powered inpainting
"""

import os
import cv2
import numpy as np
import tempfile
import shutil
from typing import List, Dict, Optional, Tuple
from logo_detector import LogoDetector
from lama_integration import LamaCleaner


class EnhancedLogoDetector(LogoDetector):
    """Enhanced logo detector with lama-cleaner integration"""
    
    def __init__(self, ffmpeg_path: str, use_lama_cleaner: bool = True):
        """
        Initialize enhanced detector
        
        Args:
            ffmpeg_path: Path to FFmpeg executable
            use_lama_cleaner: Whether to use lama-cleaner for removal
        """
        super().__init__(ffmpeg_path)
        self.use_lama_cleaner = use_lama_cleaner
        
    def remove_watermarks_advanced(self, video_path: str, output_path: str, 
                                 method: str = "auto") -> bool:
        """
        Remove watermarks using the best available method
        
        Args:
            video_path: Input video path
            output_path: Output video path
            method: 'ffmpeg', 'lama', or 'auto' (chooses best method)
            
        Returns:
            bool: True if successful
        """
        print(f"🎯 Starting advanced watermark removal: {video_path}")
        print(f"📤 Output will be saved to: {output_path}")
        
        # Detect watermarks first
        watermark_timelines = self.detect_logos_with_timeline(video_path)
        
        if not watermark_timelines:
            print("❌ No watermarks detected")
            return False
            
        print(f"✅ Detected {len(watermark_timelines)} watermark timeline(s)")
        
        # Choose removal method
        if method == "auto":
            chosen_method = self._choose_best_method(watermark_timelines, video_path)
        else:
            chosen_method = method
            
        print(f"🔧 Using removal method: {chosen_method}")
        
        # Apply chosen method
        if chosen_method == "lama" and self.use_lama_cleaner:
            return self._remove_with_lama_cleaner(video_path, output_path, watermark_timelines)
        else:
            return self._remove_with_ffmpeg(video_path, output_path, watermark_timelines)
    
    def _choose_best_method(self, watermark_timelines: List[Dict], video_path: str) -> str:
        """
        Choose the best removal method based on watermark characteristics
        
        Args:
            watermark_timelines: Detected watermark timelines
            video_path: Input video path
            
        Returns:
            str: 'lama' or 'ffmpeg'
        """
        # Analyze watermarks to decide best method
        has_moving_watermarks = any(timeline.get('is_moving', False) for timeline in watermark_timelines)
        has_complex_watermarks = any(len(timeline.get('text', '')) > 10 for timeline in watermark_timelines)
        
        # Get video duration to estimate processing time
        try:
            duration_cmd = [
                "ffprobe", "-v", "error", "-show_entries", "format=duration", 
                "-of", "default=noprint_wrappers=1:nokey=1", video_path
            ]
            import subprocess
            duration_result = subprocess.run(duration_cmd, capture_output=True, text=True)
            duration = float(duration_result.stdout.strip())
        except:
            duration = 60.0  # Default
        
        # Decision logic
        if not self.use_lama_cleaner:
            return "ffmpeg"
        
        # Use lama-cleaner for:
        # 1. Complex/large watermarks that might benefit from inpainting
        # 2. Short videos (under 30 seconds) where processing time is acceptable
        # 3. Static watermarks where quality is more important than speed
        
        if duration < 30 or has_complex_watermarks:
            return "lama"
        elif has_moving_watermarks and duration > 60:
            # Moving watermarks in long videos - FFmpeg is faster
            return "ffmpeg"
        else:
            return "lama"  # Default to lama for quality
    
    def _remove_with_lama_cleaner(self, video_path: str, output_path: str, 
                                watermark_timelines: List[Dict]) -> bool:
        """Remove watermarks using lama-cleaner"""
        print("🤖 Using AI-powered lama-cleaner for watermark removal")
        
        try:
            with LamaCleaner() as cleaner:
                success = cleaner.process_video_frames(video_path, output_path, watermark_timelines)
                
                if success:
                    print(f"✅ Lama-cleaner removal successful: {output_path}")
                else:
                    print("❌ Lama-cleaner removal failed, falling back to FFmpeg")
                    success = self._remove_with_ffmpeg(video_path, output_path, watermark_timelines)
                
                return success
                
        except Exception as e:
            print(f"❌ Lama-cleaner error: {e}")
            print("🔄 Falling back to FFmpeg method")
            return self._remove_with_ffmpeg(video_path, output_path, watermark_timelines)
    
    def _remove_with_ffmpeg(self, video_path: str, output_path: str, 
                          watermark_timelines: List[Dict]) -> bool:
        """Remove watermarks using FFmpeg (original method)"""
        print("⚡ Using FFmpeg for fast watermark removal")
        
        try:
            # Use the first (most confident) watermark timeline
            timeline = watermark_timelines[0]
            
            # Create removal command
            cmd = self.create_dynamic_removal_command(video_path, timeline, method='drawbox')
            cmd.append(output_path)
            
            print(f"🎬 Running FFmpeg command...")
            
            import subprocess
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ FFmpeg removal successful: {output_path}")
                return True
            else:
                print(f"❌ FFmpeg removal failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ FFmpeg error: {e}")
            return False
    
    def compare_removal_methods(self, video_path: str, base_output_path: str) -> Dict[str, str]:
        """
        Compare both removal methods side by side
        
        Args:
            video_path: Input video path
            base_output_path: Base path for outputs (will add suffixes)
            
        Returns:
            Dict with paths to both output files
        """
        print("🔄 Comparing removal methods...")
        
        # Generate output paths
        base_name = os.path.splitext(base_output_path)[0]
        ffmpeg_output = f"{base_name}_ffmpeg.mp4"
        lama_output = f"{base_name}_lama.mp4"
        
        results = {}
        
        # Try FFmpeg method
        print("\n1️⃣ Testing FFmpeg method...")
        if self.remove_watermarks_advanced(video_path, ffmpeg_output, method="ffmpeg"):
            results["ffmpeg"] = ffmpeg_output
            print(f"✅ FFmpeg result: {ffmpeg_output}")
        else:
            print("❌ FFmpeg method failed")
        
        # Try Lama-cleaner method  
        print("\n2️⃣ Testing Lama-cleaner method...")
        if self.remove_watermarks_advanced(video_path, lama_output, method="lama"):
            results["lama"] = lama_output
            print(f"✅ Lama-cleaner result: {lama_output}")
        else:
            print("❌ Lama-cleaner method failed")
        
        print(f"\n📊 Comparison complete. Results: {results}")
        return results
    
    def create_removal_preview(self, video_path: str, preview_path: str, 
                             duration: float = 10.0) -> bool:
        """
        Create a preview of watermark removal on a short clip
        
        Args:
            video_path: Input video path
            preview_path: Output preview path
            duration: Preview duration in seconds
            
        Returns:
            bool: True if successful
        """
        print(f"🎬 Creating {duration}s preview of watermark removal...")
        
        # Create temporary clip
        temp_clip = f"temp_preview_clip_{os.getpid()}.mp4"
        
        try:
            # Extract preview clip
            import subprocess
            extract_cmd = [
                self.ffmpeg_path, "-i", video_path,
                "-t", str(duration),
                "-c", "copy",
                temp_clip
            ]
            
            result = subprocess.run(extract_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Failed to extract preview clip: {result.stderr}")
                return False
            
            # Apply watermark removal to preview
            success = self.remove_watermarks_advanced(temp_clip, preview_path, method="auto")
            
            if success:
                print(f"✅ Preview created: {preview_path}")
            else:
                print("❌ Preview creation failed")
            
            # Clean up
            if os.path.exists(temp_clip):
                os.remove(temp_clip)
            
            return success
            
        except Exception as e:
            print(f"❌ Preview creation error: {e}")
            # Clean up
            if os.path.exists(temp_clip):
                os.remove(temp_clip)
            return False


def create_watermark_removal_demo():
    """Create a comprehensive demo of the enhanced watermark removal system"""
    
    print("🎯 Enhanced Watermark Removal Demo")
    print("=" * 50)
    
    # Check for test videos
    test_videos = [
        "test_moving_final.mp4",
        "test_simple_watermark.mp4", 
        "test_final_watermark_removal.mp4"
    ]
    
    available_videos = [v for v in test_videos if os.path.exists(v)]
    
    if not available_videos:
        print("❌ No test videos found. Please ensure you have test videos available.")
        return False
    
    test_video = available_videos[0]
    print(f"📹 Using test video: {test_video}")
    
    # Initialize enhanced detector
    ffmpeg_path = "ffmpeg"  # Assuming ffmpeg is in PATH
    detector = EnhancedLogoDetector(ffmpeg_path, use_lama_cleaner=True)
    
    # Demo 1: Quick preview
    print("\n🎬 Demo 1: Creating 10-second preview...")
    preview_path = f"demo_preview_{os.path.basename(test_video)}"
    detector.create_removal_preview(test_video, preview_path, duration=10.0)
    
    # Demo 2: Method comparison
    print("\n🔄 Demo 2: Comparing removal methods...")
    comparison_results = detector.compare_removal_methods(test_video, f"demo_comparison_{os.path.basename(test_video)}")
    
    # Demo 3: Full auto removal
    print("\n🤖 Demo 3: Full auto removal...")
    auto_output = f"demo_auto_{os.path.basename(test_video)}"
    detector.remove_watermarks_advanced(test_video, auto_output, method="auto")
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 DEMO SUMMARY")
    print("=" * 50)
    
    output_files = []
    
    if os.path.exists(preview_path):
        output_files.append(f"Preview (10s): {preview_path}")
    
    for method, path in comparison_results.items():
        if os.path.exists(path):
            output_files.append(f"Method {method}: {path}")
    
    if os.path.exists(auto_output):
        output_files.append(f"Auto removal: {auto_output}")
    
    if output_files:
        print("✅ Generated files:")
        for file in output_files:
            print(f"  • {file}")
        
        print("\n💡 Tips:")
        print("  • Compare FFmpeg vs Lama-cleaner results for quality")
        print("  • FFmpeg is faster for long videos")
        print("  • Lama-cleaner provides better quality for complex watermarks")
        print("  • Auto mode chooses the best method automatically")
        
        return True
    else:
        print("❌ No output files were generated")
        return False


if __name__ == "__main__":
    create_watermark_removal_demo()
