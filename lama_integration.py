#!/usr/bin/env python3
"""
Lama-Cleaner Integration Module
Provides advanced inpainting-based watermark removal using lama-cleaner
"""

import cv2
import numpy as np
import tempfile
import os
import subprocess
import json
from typing import List, Tuple, Optional, Dict
from pathlib import Path


class LamaCleaner:
    """Handles lama-cleaner integration for advanced watermark removal"""
    
    def __init__(self, model_name: str = "lama", use_mock: bool = False):
        """
        Initialize LamaCleaner
        
        Args:
            model_name: Model to use ('lama', 'ldm', 'zits', 'mat', 'fcf', 'cv2')
            use_mock: Force use of mock implementation for testing
        """
        self.model_name = model_name
        self.temp_dir = None
        self.use_mock = use_mock
        self._check_lama_availability()
        
    def _check_lama_availability(self):
        """Check if lama-cleaner is available"""
        if self.use_mock:
            self.available = False
            return
            
        try:
            result = subprocess.run(['lama-cleaner', '--help'], 
                                  capture_output=True, text=True, timeout=10)
            self.available = result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            self.available = False
            
        if not self.available:
            print("⚠️ lama-cleaner not available, using mock implementation")
        
    def __enter__(self):
        """Create temporary directory for processing"""
        self.temp_dir = tempfile.mkdtemp()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up temporary directory"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
    
    def remove_watermark_from_image(self, image_path: str, mask_path: str, output_path: str) -> bool:
        """
        Remove watermark from a single image using lama-cleaner or mock implementation
        
        Args:
            image_path: Path to input image
            mask_path: Path to mask image (white regions will be inpainted)
            output_path: Path for output image
            
        Returns:
            bool: True if successful
        """
        if not self.available:
            return self._mock_inpaint(image_path, mask_path, output_path)
            
        try:
            cmd = [
                "lama-cleaner",
                "--model", self.model_name,
                "--device", "cpu",  # Use CPU for compatibility
                "--input", image_path,
                "--mask", mask_path,
                "--output", output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return os.path.exists(output_path)
            
        except subprocess.CalledProcessError as e:
            print(f"Lama-cleaner failed: {e}")
            print(f"Error output: {e.stderr}")
            return False
        except Exception as e:
            print(f"Error running lama-cleaner: {e}")
            return False
    
    def create_mask_from_detections(self, image_shape: Tuple[int, int], 
                                  detections: List[Dict]) -> np.ndarray:
        """
        Create a mask from watermark detections
        
        Args:
            image_shape: (height, width) of the image
            detections: List of detection dictionaries with bbox coordinates
            
        Returns:
            np.ndarray: Binary mask (255 for watermark regions, 0 for background)
        """
        mask = np.zeros(image_shape[:2], dtype=np.uint8)
        
        for detection in detections:
            # Extract bounding box coordinates
            if 'bbox' in detection:
                x, y, w, h = detection['bbox']
            elif all(k in detection for k in ['x', 'y', 'w', 'h']):
                x, y, w, h = detection['x'], detection['y'], detection['w'], detection['h']
            else:
                continue
                
            # Ensure coordinates are within image bounds
            x = max(0, min(x, image_shape[1] - 1))
            y = max(0, min(y, image_shape[0] - 1))
            w = max(1, min(w, image_shape[1] - x))
            h = max(1, min(h, image_shape[0] - y))
            
            # Fill the bounding box region in the mask
            mask[y:y+h, x:x+w] = 255
            
        return mask
    
    def process_video_frames(self, video_path: str, output_path: str, 
                           watermark_timelines: List[Dict]) -> bool:
        """
        Process video by extracting frames, removing watermarks, and reconstructing video
        
        Args:
            video_path: Path to input video
            output_path: Path for output video
            watermark_timelines: List of watermark timeline dictionaries
            
        Returns:
            bool: True if successful
        """
        if not self.temp_dir:
            print("Error: LamaCleaner not properly initialized")
            return False
            
        try:
            # Create subdirectories
            frames_dir = os.path.join(self.temp_dir, "frames")
            masks_dir = os.path.join(self.temp_dir, "masks")
            output_frames_dir = os.path.join(self.temp_dir, "output_frames")
            
            os.makedirs(frames_dir, exist_ok=True)
            os.makedirs(masks_dir, exist_ok=True)
            os.makedirs(output_frames_dir, exist_ok=True)
            
            # Extract frames from video
            if not self._extract_frames(video_path, frames_dir):
                return False
                
            # Get video info
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.release()
            
            print(f"Processing {total_frames} frames at {fps} FPS")
            
            # Process each frame
            processed_count = 0
            for frame_num in range(total_frames):
                frame_path = os.path.join(frames_dir, f"frame_{frame_num:06d}.png")
                
                if not os.path.exists(frame_path):
                    continue
                    
                # Get watermarks for this frame
                frame_time = frame_num / fps
                frame_watermarks = self._get_watermarks_for_time(watermark_timelines, frame_time)
                
                if frame_watermarks:
                    # Create mask for this frame
                    mask = self.create_mask_from_detections((frame_height, frame_width), frame_watermarks)
                    mask_path = os.path.join(masks_dir, f"mask_{frame_num:06d}.png")
                    cv2.imwrite(mask_path, mask)
                    
                    # Apply lama-cleaner to remove watermarks
                    output_frame_path = os.path.join(output_frames_dir, f"frame_{frame_num:06d}.png")
                    if self.remove_watermark_from_image(frame_path, mask_path, output_frame_path):
                        processed_count += 1
                    else:
                        # If lama-cleaner fails, copy original frame
                        import shutil
                        shutil.copy2(frame_path, output_frame_path)
                else:
                    # No watermarks, copy original frame
                    output_frame_path = os.path.join(output_frames_dir, f"frame_{frame_num:06d}.png")
                    import shutil
                    shutil.copy2(frame_path, output_frame_path)
                    
                if frame_num % 50 == 0:
                    print(f"Processed frame {frame_num}/{total_frames}")
            
            print(f"Applied lama-cleaner to {processed_count} frames")
            
            # Reconstruct video from processed frames
            return self._reconstruct_video(output_frames_dir, output_path, fps)
            
        except Exception as e:
            print(f"Error processing video frames: {e}")
            return False
    
    def _extract_frames(self, video_path: str, frames_dir: str) -> bool:
        """Extract all frames from video"""
        try:
            cmd = [
                "ffmpeg", "-i", video_path,
                "-vf", "fps=fps",  # Extract at original FPS
                os.path.join(frames_dir, "frame_%06d.png")
            ]
            
            subprocess.run(cmd, capture_output=True, check=True)
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Failed to extract frames: {e}")
            return False
    
    def _reconstruct_video(self, frames_dir: str, output_path: str, fps: float) -> bool:
        """Reconstruct video from processed frames"""
        try:
            cmd = [
                "ffmpeg", "-y",
                "-framerate", str(fps),
                "-i", os.path.join(frames_dir, "frame_%06d.png"),
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                output_path
            ]
            
            subprocess.run(cmd, capture_output=True, check=True)
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Failed to reconstruct video: {e}")
            return False
    
    def _get_watermarks_for_time(self, watermark_timelines: List[Dict], 
                               current_time: float) -> List[Dict]:
        """Get watermarks that should be present at a specific time"""
        watermarks = []
        
        for timeline in watermark_timelines:
            if 'detections' not in timeline:
                continue
                
            # Check if this timeline is active at current time
            timeline_active = False
            
            for detection in timeline['detections']:
                start_time = detection.get('start_time', 0)
                end_time = detection.get('end_time', float('inf'))
                
                if start_time <= current_time <= end_time:
                    timeline_active = True
                    break
            
            if timeline_active:
                # Find the detection closest to current time
                best_detection = None
                min_time_diff = float('inf')
                
                for detection in timeline['detections']:
                    detection_time = detection.get('time', 0)
                    time_diff = abs(current_time - detection_time)
                    
                    if time_diff < min_time_diff:
                        min_time_diff = time_diff
                        best_detection = detection
                
                if best_detection:
                    watermarks.append(best_detection)
        
        return watermarks
    
    def _mock_inpaint(self, image_path: str, mask_path: str, output_path: str) -> bool:
        """
        Mock inpainting implementation using OpenCV's telea algorithm
        
        Args:
            image_path: Path to input image
            mask_path: Path to mask image
            output_path: Path for output image
            
        Returns:
            bool: True if successful
        """
        try:
            # Load image and mask
            image = cv2.imread(image_path)
            mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
            
            if image is None or mask is None:
                print(f"Failed to load image or mask: {image_path}, {mask_path}")
                return False
            
            # Use OpenCV's inpainting (Telea algorithm)
            # This is a simple but effective inpainting method
            result = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
            
            # For better results with watermarks, apply some additional processing
            # Blur the inpainted regions slightly to blend better
            kernel = np.ones((3,3), np.float32) / 9
            blurred = cv2.filter2D(result, -1, kernel)
            
            # Only apply blur to the masked regions
            mask_norm = mask.astype(np.float32) / 255.0
            mask_norm = np.stack([mask_norm] * 3, axis=2)
            
            result = result.astype(np.float32)
            blurred = blurred.astype(np.float32)
            
            # Blend original and blurred based on mask
            final_result = result * (1 - mask_norm * 0.3) + blurred * (mask_norm * 0.3)
            final_result = np.clip(final_result, 0, 255).astype(np.uint8)
            
            # Save result
            success = cv2.imwrite(output_path, final_result)
            
            if success:
                print(f"✅ Mock inpainting successful: {output_path}")
            else:
                print(f"❌ Failed to save mock inpaint result: {output_path}")
                
            return success
            
        except Exception as e:
            print(f"❌ Mock inpaint error: {e}")
            return False


def create_simple_mask_demo():
    """Create a simple demo showing how to use lama-cleaner for watermark removal"""
    
    # Create a test image with a simulated watermark
    test_image = np.ones((400, 600, 3), dtype=np.uint8) * 240  # Light gray background
    
    # Add some content
    cv2.rectangle(test_image, (50, 50), (550, 150), (100, 150, 200), -1)
    cv2.putText(test_image, "Original Content", (200, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Add a watermark
    cv2.rectangle(test_image, (400, 250), (580, 320), (50, 50, 50), -1)
    cv2.putText(test_image, "WATERMARK", (410, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Create mask for the watermark
    mask = np.zeros((400, 600), dtype=np.uint8)
    cv2.rectangle(mask, (400, 250), (580, 320), 255, -1)
    
    # Save test files
    test_image_path = "test_image_with_watermark.png"
    mask_path = "test_watermark_mask.png"
    output_path = "test_image_cleaned.png"
    
    cv2.imwrite(test_image_path, test_image)
    cv2.imwrite(mask_path, mask)
    
    print(f"Created test image: {test_image_path}")
    print(f"Created mask: {mask_path}")
    
    # Use lama-cleaner to remove watermark
    with LamaCleaner() as cleaner:
        success = cleaner.remove_watermark_from_image(test_image_path, mask_path, output_path)
        
        if success:
            print(f"Watermark removal successful! Output: {output_path}")
        else:
            print("Watermark removal failed")
    
    return success


if __name__ == "__main__":
    print("Testing Lama-Cleaner Integration...")
    create_simple_mask_demo()
