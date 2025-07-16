import subprocess
import os
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal


class WorkerThread(QThread):
    progress = pyqtSignal(str)  # For log messages
    finished = pyqtSignal(bool, str)  # For completion (success, message)
    
    def __init__(self, operation_type, *args):
        super().__init__()
        self.operation_type = operation_type
        self.args = args
        
    def run(self):
        try:
            if self.operation_type == "download":
                self.download_video_worker(*self.args)
            elif self.operation_type == "flip":
                self.flip_video_worker(*self.args)
            elif self.operation_type == "flip_folder":
                self.flip_folder_worker(*self.args)
            elif self.operation_type == "split":
                self.split_video_worker(*self.args)
            elif self.operation_type == "convert":
                self.convert_to_reel_worker(*self.args)
            elif self.operation_type == "remove_logo":
                self.remove_logo_worker(*self.args)
            elif self.operation_type == "dynamic_removal":
                self.dynamic_removal_worker(*self.args)
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")
    
    def download_video_worker(self, ytdlp_path, url, save_path):
        self.progress.emit(f"Starting download for: {url}")
        cmd = [ytdlp_path, "-f", "best", "-P", save_path, url]
        self.progress.emit(f"Running command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            self.finished.emit(True, "Download completed successfully!")
        else:
            self.finished.emit(False, f"Download failed: {result.stderr}")
    
    def flip_video_worker(self, ffmpeg_path, file_path, filter_param, output_path, flip_choice):
        self.progress.emit(f"Flipping video ({flip_choice}): {file_path}")
        cmd = [ffmpeg_path, "-i", file_path, "-vf", filter_param, "-c:a", "copy", output_path]
        self.progress.emit(f"Running command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            self.finished.emit(True, f"Flip completed! Saved to: {output_path}")
        else:
            self.finished.emit(False, f"Flip failed: {result.stderr}")
    
    def flip_folder_worker(self, ffmpeg_path, video_files, filter_param, output_folder, suffix):
        successful_flips = 0
        failed_flips = 0
        total_files = len(video_files)
        
        for i, file_path in enumerate(video_files):
            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)
            output_path = os.path.join(output_folder, f"{name}{suffix}{ext}")
            
            self.progress.emit(f"[{i+1}/{total_files}] Flipping: {filename}")
            
            cmd = [ffmpeg_path, "-i", file_path, "-vf", filter_param, "-c:a", "copy", output_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.progress.emit(f"✓ Successfully flipped: {filename}")
                successful_flips += 1
            else:
                self.progress.emit(f"✗ Failed to flip {filename}: {result.stderr}")
                failed_flips += 1
        
        self.finished.emit(True, f"Folder flip completed! Success: {successful_flips}, Failed: {failed_flips}")
    
    def split_video_worker(self, ffmpeg_path, file_path, segment_time, output_pattern):
        self.progress.emit(f"Splitting video into {segment_time//60} minute parts...")
        
        # Use proper segmenting command that re-encodes to ensure clean splits
        cmd = [
            ffmpeg_path, 
            "-i", file_path,
            "-c:v", "libx264",  # Re-encode video for clean splits
            "-c:a", "aac",      # Re-encode audio for compatibility
            "-map", "0",
            "-f", "segment",
            "-segment_time", str(segment_time),
            "-reset_timestamps", "1",  # Reset timestamps for each segment
            "-avoid_negative_ts", "make_zero",  # Avoid negative timestamps
            output_pattern
        ]
        
        self.progress.emit(f"Running command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            # Count the number of parts created
            import glob
            output_dir = os.path.dirname(output_pattern)
            parts = glob.glob(os.path.join(output_dir, "part_*.mp4"))
            self.finished.emit(True, f"Split completed successfully! Created {len(parts)} parts.")
        else:
            self.finished.emit(False, f"Split failed: {result.stderr}")
    
    def convert_to_reel_worker(self, ffmpeg_path, video_files, folder_path):
        successful_conversions = 0
        failed_conversions = 0
        total_files = len(video_files)
        
        for file_idx, video_file in enumerate(video_files):
            filename = os.path.basename(video_file)
            base_name = os.path.splitext(filename)[0]
            
            output_folder = os.path.join(folder_path, f"{base_name}_converted")
            os.makedirs(output_folder, exist_ok=True)
            
            self.progress.emit(f"[{file_idx+1}/{total_files}] Converting: {filename}")
            
            # Get video duration
            try:
                duration_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_file]
                duration_result = subprocess.run(duration_cmd, capture_output=True, text=True, check=True)
                duration = int(float(duration_result.stdout.strip()))
                self.progress.emit(f"Video duration: {duration} seconds")
            except subprocess.CalledProcessError as e:
                self.progress.emit(f"✗ Failed to get duration for {filename}: {e}")
                failed_conversions += 1
                continue

            start = 0
            count = 0
            total_parts = (duration + 599) // 600  # Calculate total parts needed

            while start < duration:
                chunk = min(600, duration - start)
                output_path = os.path.join(output_folder, f"{base_name}_part{count}_tiktok.mp4")
                
                self.progress.emit(f"Creating part {count+1}/{total_parts} from {start}s for {chunk}s")

                cmd = [
                    ffmpeg_path, "-ss", str(start), "-i", video_file, "-t", str(chunk),
                    "-filter_complex",
                    "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,boxblur=10:1[bg];"
                    "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease[fg];"
                    "[bg][fg]overlay=(W-w)/2:(H-h)/2,crop=1080:1920",
                    "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-c:a", "copy",
                    output_path
                ]

                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    self.progress.emit(f"✓ Successfully created part {count+1}")
                else:
                    self.progress.emit(f"✗ Failed to create part {count+1}: {result.stderr}")
                    failed_conversions += 1
                    break

                start += 600
                count += 1

            if start >= duration:
                self.progress.emit(f"✅ Done: {base_name} → Folder: {output_folder}")
                successful_conversions += 1
            else:
                failed_conversions += 1

        self.finished.emit(True, f"Conversion completed! Success: {successful_conversions}, Failed: {failed_conversions}")
    
    def remove_logo_worker(self, ffmpeg_path, file_path, method_type, logo_position, output_path):
        self.progress.emit(f"Removing logo using {method_type} method...")
        
        # Get video dimensions first for coordinate validation
        try:
            probe_cmd = [
                "ffprobe", "-v", "error", "-select_streams", "v:0", 
                "-show_entries", "stream=width,height", "-of", "csv=p=0", file_path
            ]
            probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
            if probe_result.returncode == 0:
                dimensions = probe_result.stdout.strip().split(',')
                video_width = int(dimensions[0])
                video_height = int(dimensions[1])
                self.progress.emit(f"Video dimensions: {video_width}x{video_height}")
            else:
                # Fallback dimensions if probe fails
                video_width, video_height = 1920, 1080
                self.progress.emit("Warning: Could not detect video dimensions, using fallback 1920x1080")
        except Exception as e:
            video_width, video_height = 1920, 1080
            self.progress.emit(f"Warning: Error detecting video dimensions: {e}, using fallback 1920x1080")
        
        # Build the filter based on method type
        x = logo_position["x"]
        y = logo_position["y"] 
        w = logo_position["width"]
        h = logo_position["height"]
        
        # Add padding for text watermarks to ensure complete coverage
        padding = 5
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = w + (2 * padding)
        h = h + (2 * padding)
        
        # Validate coordinates against video dimensions
        if x >= video_width or y >= video_height:
            self.finished.emit(False, f"Error: Logo position ({x}, {y}) is outside video frame ({video_width}x{video_height})")
            return
        
        # Clamp coordinates to video boundaries and ensure delogo filter compatibility
        # The delogo filter requires that x+w and y+h are strictly within the frame
        x = max(0, min(x, video_width - 1))
        y = max(0, min(y, video_height - 1))
        
        # Adjust width and height to ensure they don't exceed frame boundaries
        max_w = video_width - x  # Maximum width from current x position
        max_h = video_height - y  # Maximum height from current y position
        w = min(w, max_w - 1)  # Leave 1 pixel margin to avoid exactly hitting boundary
        h = min(h, max_h - 1)  # Leave 1 pixel margin to avoid exactly hitting boundary
        
        # Ensure minimum size (delogo filter needs at least a few pixels)
        if w < 2 or h < 2:
            self.finished.emit(False, f"Error: Logo area too small after validation: {w}x{h} (minimum: 2x2)")
            return
        
        self.progress.emit(f"Using validated coordinates: x={x}, y={y}, w={w}, h={h}")
        
        if method_type == "blur":
            # Enhanced blur for text watermarks and moving content
            if logo_position.get('type') == 'moving_watermark':
                # Stronger blur for moving watermarks
                self.progress.emit("Using enhanced blur for moving watermark...")
                filter_complex = f"[0:v]crop={w}:{h}:{x}:{y},gblur=sigma=20[blurred];[0:v][blurred]overlay={x}:{y}[out]"
            else:
                # Standard blur for static watermarks
                filter_complex = f"[0:v]crop={w}:{h}:{x}:{y},gblur=sigma=15[blurred];[0:v][blurred]overlay={x}:{y}[out]"
            
            cmd = [
                ffmpeg_path, "-i", file_path,
                "-filter_complex", filter_complex,
                "-map", "[out]", "-map", "0:a?",
                "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-c:a", "copy",
                output_path
            ]
        elif method_type == "blackout":
            # Enhanced blackout with slight transparency for better blending
            vf_filter = f"drawbox=x={x}:y={y}:w={w}:h={h}:color=black@0.8:t=fill"
            cmd = [
                ffmpeg_path, "-i", file_path,
                "-vf", vf_filter,
                "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-c:a", "copy",
                output_path
            ]
        elif method_type == "pixelate":
            # Enhanced pixelation for text removal
            pixel_factor = max(1, min(w, h) // 8)  # Adaptive pixelation
            filter_complex = f"[0:v]crop={w}:{h}:{x}:{y},scale={w//pixel_factor}:{h//pixel_factor},scale={w}:{h}:flags=neighbor[pixelated];[0:v][pixelated]overlay={x}:{y}[out]"
            cmd = [
                ffmpeg_path, "-i", file_path,
                "-filter_complex", filter_complex,
                "-map", "[out]", "-map", "0:a?",
                "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-c:a", "copy",
                output_path
            ]
        elif method_type == "inpaint":
            # Enhanced inpainting for text and moving watermarks
            if logo_position.get('type') == 'moving_watermark':
                # For moving watermarks, use more aggressive inpainting
                self.progress.emit("Using advanced inpainting for moving watermark...")
                filter_complex = f"[0:v]crop={w}:{h}:{x}:{y},median=7,gblur=sigma=2[cleaned];[0:v][cleaned]overlay={x}:{y}[out]"
            elif logo_position.get('type') == 'combined_watermarks':
                # For combined watermarks, use stronger inpainting
                watermark_count = logo_position.get('watermark_count', 1)
                self.progress.emit(f"Using enhanced inpainting for {watermark_count} combined watermarks...")
                filter_complex = f"[0:v]crop={w}:{h}:{x}:{y},median=9,gblur=sigma=3[cleaned];[0:v][cleaned]overlay={x}:{y}[out]"
            else:
                # Standard inpainting for static watermarks
                filter_complex = f"[0:v]crop={w}:{h}:{x}:{y},median=5[cleaned];[0:v][cleaned]overlay={x}:{y}[out]"
            
            cmd = [
                ffmpeg_path, "-i", file_path,
                "-filter_complex", filter_complex,
                "-map", "[out]", "-map", "0:a?",
                "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-c:a", "copy",
                output_path
            ]
        elif method_type == "lama":
            # Use lama-cleaner for AI-based inpainting
            self.progress.emit("Using Lama-Cleaner for AI inpainting...")
            
            try:
                # Import lama integration
                from lama_integration import LamaCleaner
                import cv2
                import tempfile
                
                # Extract a representative frame to test the watermark area
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_frame:
                    frame_path = temp_frame.name
                
                # Extract frame at middle of video
                extract_cmd = [
                    ffmpeg_path, "-i", file_path, 
                    "-ss", "00:00:05", "-vframes", "1", 
                    "-y", frame_path
                ]
                
                extract_result = subprocess.run(extract_cmd, capture_output=True, text=True)
                if extract_result.returncode != 0:
                    self.finished.emit(False, f"Failed to extract frame for lama-cleaner: {extract_result.stderr}")
                    return
                
                # Create mask for the watermark area
                frame = cv2.imread(frame_path)
                if frame is None:
                    self.finished.emit(False, "Failed to read extracted frame")
                    return
                
                # Create mask
                mask = np.zeros(frame.shape[:2], dtype=np.uint8)
                cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)
                
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_mask:
                    mask_path = temp_mask.name
                
                cv2.imwrite(mask_path, mask)
                
                # Test lama-cleaner on the frame
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_output:
                    test_output_path = temp_output.name
                
                with LamaCleaner(model_name="lama") as cleaner:
                    success = cleaner.remove_watermark_from_image(frame_path, mask_path, test_output_path)
                
                if not success:
                    self.progress.emit("Lama-cleaner failed on test frame, falling back to enhanced inpainting...")
                    # Fallback to enhanced inpainting
                    filter_complex = f"[0:v]crop={w}:{h}:{x}:{y},median=9,gblur=sigma=3[cleaned];[0:v][cleaned]overlay={x}:{y}[out]"
                    cmd = [
                        ffmpeg_path, "-i", file_path,
                        "-filter_complex", filter_complex,
                        "-map", "[out]", "-map", "0:a?",
                        "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-c:a", "copy",
                        output_path
                    ]
                else:
                    self.progress.emit("Lama-cleaner test successful! Processing full video...")
                    # For now, fall back to enhanced inpainting for video processing
                    # Full video lama-cleaner processing would require significant time and resources
                    self.progress.emit("Note: Using enhanced inpainting for video processing (lama-cleaner for video is very slow)")
                    filter_complex = f"[0:v]crop={w}:{h}:{x}:{y},median=9,gblur=sigma=4[cleaned];[0:v][cleaned]overlay={x}:{y}[out]"
                    cmd = [
                        ffmpeg_path, "-i", file_path,
                        "-filter_complex", filter_complex,
                        "-map", "[out]", "-map", "0:a?",
                        "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-c:a", "copy",
                        output_path
                    ]
                
                # Clean up temp files
                for temp_file in [frame_path, mask_path, test_output_path]:
                    try:
                        os.unlink(temp_file)
                    except:
                        pass
                        
            except ImportError:
                self.progress.emit("Lama-cleaner not available, falling back to enhanced inpainting...")
                filter_complex = f"[0:v]crop={w}:{h}:{x}:{y},median=9,gblur=sigma=3[cleaned];[0:v][cleaned]overlay={x}:{y}[out]"
                cmd = [
                    ffmpeg_path, "-i", file_path,
                    "-filter_complex", filter_complex,
                    "-map", "[out]", "-map", "0:a?",
                    "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-c:a", "copy",
                    output_path
                ]
            except Exception as e:
                self.progress.emit(f"Error with lama-cleaner: {e}, falling back to enhanced inpainting...")
                filter_complex = f"[0:v]crop={w}:{h}:{x}:{y},median=9,gblur=sigma=3[cleaned];[0:v][cleaned]overlay={x}:{y}[out]"
                cmd = [
                    ffmpeg_path, "-i", file_path,
                    "-filter_complex", filter_complex,
                    "-map", "[out]", "-map", "0:a?",
                    "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-c:a", "copy",
                    output_path
                ]
        else:  # delogo
            # Enhanced delogo with show parameter for better text removal
            vf_filter = f"delogo=x={x}:y={y}:w={w}:h={h}:show=0"
            cmd = [
                ffmpeg_path, "-i", file_path,
                "-vf", vf_filter,
                "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-c:a", "copy",
                output_path
            ]
        
        self.progress.emit(f"Running command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            self.finished.emit(True, f"Logo removal completed! Saved to: {output_path}")
        else:
            self.finished.emit(False, f"Logo removal failed: {result.stderr}")
    
    def dynamic_removal_worker(self, cmd, output_path):
        """Execute dynamic removal command with time-based filters"""
        self.progress.emit("Executing dynamic watermark removal with time-based filters...")
        self.progress.emit(f"Command: {' '.join(cmd)}")
        
        # Run the dynamic command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            self.finished.emit(True, f"Dynamic removal completed! Saved to: {output_path}")
        else:
            self.finished.emit(False, f"Dynamic removal failed: {result.stderr}")
