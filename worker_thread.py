import subprocess
import os
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
        cmd = [ffmpeg_path, "-i", file_path, "-c", "copy", "-map", "0", "-f", "segment", "-segment_time", str(segment_time), output_pattern]
        self.progress.emit(f"Running command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            self.finished.emit(True, "Split completed successfully!")
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
