import os
from PyQt6.QtWidgets import QInputDialog, QFileDialog, QMessageBox
from worker_thread import WorkerThread


class VideoOperations:
    """Handles all video processing operations"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        
    @property
    def ffmpeg_path(self):
        return self.main_window.ffmpeg_path
        
    @property
    def ytdlp_path(self):
        return self.main_window.ytdlp_path
    
    def download_video(self):
        """Download video from URL"""
        if not self.ytdlp_path:
            self.main_window.show_error("yt-dlp executable not found. Cannot download.")
            return

        url = self.main_window.url_input.text().strip()
        if not url:
            self.main_window.log_message("Please enter a valid URL.")
            return

        save_path = self.main_window.download_folder if self.main_window.download_folder else "."
        
        self.main_window.start_operation("Downloading Video")
        
        # Create and start worker thread
        self.main_window.worker_thread = WorkerThread("download", self.ytdlp_path, url, save_path)
        self.main_window.worker_thread.progress.connect(self.main_window.log_message)
        self.main_window.worker_thread.finished.connect(self.main_window.finish_operation)
        self.main_window.worker_thread.start()

    def flip_video(self):
        """Flip a single video file"""
        if not self.ffmpeg_path:
            self.main_window.show_error("ffmpeg executable not found. Cannot flip video.")
            return

        file_path, _ = QFileDialog.getOpenFileName(self.main_window, "Select video to flip")
        if not file_path:
            self.main_window.log_message("No video file selected.")
            return

        if not os.path.isfile(file_path):
            self.main_window.show_error("Selected video file does not exist.")
            return

        # Let user choose flip direction
        flip_options = ["Horizontal (hflip)", "Vertical (vflip)", "Both (hflip,vflip)"]
        flip_choice, ok = QInputDialog.getItem(self.main_window, "Select Flip Direction", 
                                              "Choose how to flip the video:", 
                                              flip_options, 0, False)
        if not ok:
            self.main_window.log_message("Flip operation cancelled.")
            return

        # Map choice to ffmpeg filter
        filter_param, suffix = self._get_flip_params(flip_choice)
        output_path = file_path.rsplit(".", 1)[0] + suffix + ".mp4"
        
        self.main_window.start_operation("Flipping Video")
        
        # Create and start worker thread
        self.main_window.worker_thread = WorkerThread("flip", self.ffmpeg_path, file_path, filter_param, output_path, flip_choice)
        self.main_window.worker_thread.progress.connect(self.main_window.log_message)
        self.main_window.worker_thread.finished.connect(self.main_window.finish_operation)
        self.main_window.worker_thread.start()

    def flip_folder_videos(self):
        """Flip all videos in a folder"""
        if not self.ffmpeg_path:
            self.main_window.show_error("ffmpeg executable not found. Cannot flip videos.")
            return

        folder_path = QFileDialog.getExistingDirectory(self.main_window, "Select folder containing videos to flip")
        if not folder_path:
            self.main_window.log_message("No folder selected.")
            return

        # Let user choose flip direction
        flip_options = ["Horizontal (hflip)", "Vertical (vflip)", "Both (hflip,vflip)"]
        flip_choice, ok = QInputDialog.getItem(self.main_window, "Select Flip Direction", 
                                              "Choose how to flip all videos:", 
                                              flip_options, 0, False)
        if not ok:
            self.main_window.log_message("Flip operation cancelled.")
            return

        # Map choice to ffmpeg filter and suffix
        filter_param, suffix = self._get_flip_params(flip_choice)

        # Find video files
        video_files = self._find_video_files(folder_path)
        if not video_files:
            self.main_window.log_message("No video files found in the selected folder.")
            return

        # Create output folder for flipped videos
        output_folder = os.path.join(folder_path, f"flipped_videos_{suffix[1:]}")  # Remove underscore from suffix
        os.makedirs(output_folder, exist_ok=True)
        
        self.main_window.start_operation(f"Flipping {len(video_files)} Videos")
        
        # Create and start worker thread
        self.main_window.worker_thread = WorkerThread("flip_folder", self.ffmpeg_path, video_files, filter_param, output_folder, suffix)
        self.main_window.worker_thread.progress.connect(self.main_window.log_message)
        self.main_window.worker_thread.finished.connect(self.main_window.finish_operation)
        self.main_window.worker_thread.start()

    def split_video(self):
        """Split a video into smaller parts"""
        if not self.ffmpeg_path:
            self.main_window.show_error("ffmpeg executable not found. Cannot split video.")
            return

        file_path, _ = QFileDialog.getOpenFileName(self.main_window, "Select video to split")
        if not file_path:
            self.main_window.log_message("No video file selected.")
            return

        if not os.path.isfile(file_path):
            self.main_window.show_error("Selected video file does not exist.")
            return

        # Let user choose split duration
        segment_time, duration_name = self._get_split_duration()
        if segment_time is None:
            return

        output_folder = file_path.rsplit(".", 1)[0] + f"_parts_{duration_name}"
        os.makedirs(output_folder, exist_ok=True)
        output_pattern = os.path.join(output_folder, "part_%03d.mp4")

        self.main_window.start_operation(f"Splitting Video ({duration_name} parts)")
        
        # Create and start worker thread
        self.main_window.worker_thread = WorkerThread("split", self.ffmpeg_path, file_path, segment_time, output_pattern)
        self.main_window.worker_thread.progress.connect(self.main_window.log_message)
        self.main_window.worker_thread.finished.connect(self.main_window.finish_operation)
        self.main_window.worker_thread.start()

    def convert_to_reel(self):
        """Convert videos to TikTok/Reel format"""
        if not self.ffmpeg_path:
            self.main_window.show_error("ffmpeg executable not found. Cannot convert video.")
            return

        folder_path = QFileDialog.getExistingDirectory(self.main_window, "Select folder containing videos to convert to TikTok/Reel format")
        if not folder_path:
            self.main_window.log_message("No folder selected.")
            return

        # Find video files
        video_files = self._find_video_files(folder_path)
        if not video_files:
            self.main_window.log_message("No video files found in the selected folder.")
            return

        self.main_window.start_operation(f"Converting {len(video_files)} Videos to TikTok/Reel")
        
        # Create and start worker thread
        self.main_window.worker_thread = WorkerThread("convert", self.ffmpeg_path, video_files, folder_path)
        self.main_window.worker_thread.progress.connect(self.main_window.log_message)
        self.main_window.worker_thread.finished.connect(self.main_window.finish_operation)
        self.main_window.worker_thread.start()

    def _get_flip_params(self, flip_choice):
        """Get ffmpeg filter parameters for flip choice"""
        if flip_choice == "Horizontal (hflip)":
            return "hflip", "_hflipped"
        elif flip_choice == "Vertical (vflip)":
            return "vflip", "_vflipped"
        else:  # Both
            return "hflip,vflip", "_hvflipped"

    def _get_split_duration(self):
        """Get split duration from user input"""
        duration_options = [
            "5 minutes (300 seconds)",
            "10 minutes (600 seconds)", 
            "15 minutes (900 seconds)",
            "20 minutes (1200 seconds)",
            "30 minutes (1800 seconds)",
            "Custom duration"
        ]
        
        duration_choice, ok = QInputDialog.getItem(self.main_window, "Select Split Duration", 
                                                  "Choose how long each part should be:", 
                                                  duration_options, 1, False)  # Default to 10 minutes
        if not ok:
            self.main_window.log_message("Split operation cancelled.")
            return None, None

        # Get the duration in seconds
        duration_map = {
            "5 minutes (300 seconds)": (300, "5min"),
            "10 minutes (600 seconds)": (600, "10min"),
            "15 minutes (900 seconds)": (900, "15min"),
            "20 minutes (1200 seconds)": (1200, "20min"),
            "30 minutes (1800 seconds)": (1800, "30min")
        }
        
        if duration_choice in duration_map:
            return duration_map[duration_choice]
        else:  # Custom duration
            # Enhanced custom duration input with decimal support
            custom_input, ok = QInputDialog.getText(
                self.main_window, 
                "Custom Duration", 
                "Enter duration in minutes (e.g., 2.5 for 2 minutes 30 seconds):\n"
                "Range: 0.1 to 180 minutes",
                text="10.0"
            )
            if not ok:
                self.main_window.log_message("Split operation cancelled.")
                return None, None
            
            try:
                custom_minutes = float(custom_input.strip())
                
                # Validate input range
                if custom_minutes < 0.1:
                    self.main_window.show_error("Duration must be at least 0.1 minutes (6 seconds).")
                    return None, None
                elif custom_minutes > 180:
                    self.main_window.show_error("Duration cannot exceed 180 minutes (3 hours).")
                    return None, None
                
                # Convert to seconds
                custom_seconds = int(custom_minutes * 60)
                
                # Create descriptive name
                if custom_minutes == int(custom_minutes):
                    duration_name = f"{int(custom_minutes)}min"
                else:
                    duration_name = f"{custom_minutes}min"
                
                self.main_window.log_message(f"Custom duration set: {custom_minutes} minutes ({custom_seconds} seconds)")
                return custom_seconds, duration_name
                
            except ValueError:
                self.main_window.show_error("Invalid input. Please enter a valid number (e.g., 2.5).")
                return None, None

    def _find_video_files(self, folder_path):
        """Find all video files in a folder"""
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v'}
        
        video_files = []
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(filename.lower())
                if ext in video_extensions:
                    video_files.append(file_path)
        
        return video_files
