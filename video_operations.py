import os
import subprocess
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

    def remove_logo(self):
        """Remove or blur logo from video with automatic detection"""
        if not self.ffmpeg_path:
            self.main_window.show_error("ffmpeg executable not found. Cannot process video.")
            return

        file_path, _ = QFileDialog.getOpenFileName(self.main_window, "Select video to remove logo from")
        if not file_path:
            self.main_window.log_message("No video file selected.")
            return

        if not os.path.isfile(file_path):
            self.main_window.show_error("Selected video file does not exist.")
            return

        # Ask user if they want automatic detection or manual positioning
        detection_options = [
            "🤖 Automatic detection (AI finds logos)",
            "📍 Manual positioning (you specify location)"
        ]
        
        detection_choice, ok = QInputDialog.getItem(self.main_window, "Logo Detection Method", 
                                                   "How would you like to detect the logo?", 
                                                   detection_options, 0, False)
        if not ok:
            self.main_window.log_message("Logo removal operation cancelled.")
            return

        if "Automatic" in detection_choice:
            self._remove_logo_automatic(file_path)
        else:
            self._remove_logo_manual(file_path)
    
    def _remove_logo_automatic(self, file_path):
        """Remove logo using automatic detection - enhanced for moving watermarks"""
        self.main_window.log_message("🔍 Analyzing video for logos with timeline tracking...")
        
        try:
            # Import logo detection (only when needed)
            from logo_detector import LogoDetector
            
            # Create detector and analyze with timeline
            detector = LogoDetector(self.ffmpeg_path)
            watermark_timelines = detector.detect_logos_with_timeline(file_path, sample_interval=2.0)
            
            if not watermark_timelines:
                self.main_window.show_error("No logos detected automatically. Try manual positioning.")
                return
            
            # Filter out excessive detections (likely false positives)
            if len(watermark_timelines) > 50:
                self.main_window.log_message(f"⚠️ Found {len(watermark_timelines)} detections - filtering to top candidates...")
                # Sort by confidence and watermark indicators, take top 10
                watermark_timelines.sort(key=lambda t: (
                    t.get('confidence', 0) * (2.0 if t.get('is_watermark', False) else 1.0),
                    len(t.get('positions', []))
                ), reverse=True)
                watermark_timelines = watermark_timelines[:10]
                self.main_window.log_message(f"📊 Filtered to {len(watermark_timelines)} most likely watermarks")
            
            self.main_window.log_message(f"✅ Found {len(watermark_timelines)} watermark timelines to remove")
            
            # Analyze each watermark timeline  
            for i, timeline in enumerate(watermark_timelines[:5]):  # Show only top 5
                is_moving = timeline.get('is_moving', False)
                position_count = len(timeline.get('positions', []))
                text = timeline.get('text', 'Unknown')[:20]
                confidence = timeline.get('confidence', 0)
                is_watermark = timeline.get('is_watermark', False)
                
                status_icon = "🎯" if is_moving else "📍"
                watermark_icon = "💧" if is_watermark else ""
                movement_text = f"({position_count} positions)" if is_moving else "(consistent position)"
                
                self.main_window.log_message(f"{status_icon} {watermark_icon}'{text}' - conf: {confidence:.2f} {movement_text}")
            
            if len(watermark_timelines) > 5:
                self.main_window.log_message(f"... and {len(watermark_timelines) - 5} more watermarks")
            
            # Remove watermarks based on their movement characteristics
            self._remove_timeline_watermarks(file_path, watermark_timelines)
                
        except ImportError:
            self.main_window.show_error("Automatic detection requires additional packages. Install: pip install opencv-python numpy")
            self.main_window.log_message("❌ Missing packages for automatic detection. Using manual mode...")
            self._remove_logo_manual(file_path)
        except Exception as e:
            self.main_window.show_error(f"Automatic detection failed: {str(e)}")
            self.main_window.log_message("❌ Automatic detection failed. Try manual positioning.")
    
    def _remove_single_watermark(self, file_path, selected_logo):
        """Remove a single watermark (original method)"""
        # Get corner info safely
        corner_info = selected_logo.get('corner', 'auto-detected')
        logo_type = selected_logo.get('type', 'unknown')
        
        self.main_window.log_message(f"🎯 Removing watermark: {corner_info} ({selected_logo['width']}x{selected_logo['height']}, confidence: {selected_logo['confidence']:.2f})")
        
        # Show watermark text if detected
        if 'text' in selected_logo:
            watermark_text = selected_logo['text'][:30] + ('...' if len(selected_logo['text']) > 30 else '')
            self.main_window.log_message(f"📝 Target text: '{watermark_text}'")
        
        # Automatically choose the best removal method based on logo type
        if 'ocr_' in logo_type or selected_logo.get('is_watermark', False):
            method_choice = "Smart inpaint (recommended for text)"
            self.main_window.log_message("🎯 Text watermark detected - using Smart Inpaint method")
        elif 'text' in logo_type or 'website' in logo_type:
            method_choice = "Smart inpaint (recommended for text)"
            self.main_window.log_message("🎯 Text content detected - using Smart Inpaint method")
        elif selected_logo['confidence'] > 0.7:
            method_choice = "Remove with delogo filter"
            self.main_window.log_message("🎯 High confidence detection - using Delogo method")
        else:
            method_choice = "Blur logo area"
            self.main_window.log_message("🎯 Standard detection - using Blur method")
        
        method_type = self._get_logo_removal_method(method_choice)
        output_path = file_path.rsplit(".", 1)[0] + f"_logo_removed_auto.mp4"
        
        self.main_window.start_operation(f"Auto-Removing Logo ({method_choice})")
        
        # Create and start worker thread
        self.main_window.worker_thread = WorkerThread("remove_logo", self.ffmpeg_path, file_path, 
                                                     method_type, selected_logo, output_path)
        self.main_window.worker_thread.progress.connect(self.main_window.log_message)
        self.main_window.worker_thread.finished.connect(self.main_window.finish_operation)
        self.main_window.worker_thread.start()
    
    def _remove_moving_watermarks(self, file_path, detected_logos):
        """Remove multiple or moving watermarks"""
        self.main_window.log_message("🎬 Detected moving/multiple watermarks - using advanced removal")
        
        # Group watermarks by position similarity
        watermark_groups = self._group_watermarks_by_position(detected_logos)
        
        if len(watermark_groups) == 1:
            # Single moving watermark - use temporal removal
            self._remove_single_moving_watermark(file_path, watermark_groups[0])
        else:
            # Multiple watermarks - remove each one
            self._remove_multiple_watermarks(file_path, watermark_groups)
    
    def _group_watermarks_by_position(self, watermarks):
        """Group watermarks that are in similar positions"""
        groups = []
        threshold = 100  # pixels threshold for grouping
        
        for watermark in watermarks:
            x, y = watermark['x'], watermark['y']
            
            # Find if this watermark belongs to an existing group
            found_group = False
            for group in groups:
                group_x = sum(w['x'] for w in group) / len(group)
                group_y = sum(w['y'] for w in group) / len(group)
                
                if abs(x - group_x) < threshold and abs(y - group_y) < threshold:
                    group.append(watermark)
                    found_group = True
                    break
            
            if not found_group:
                groups.append([watermark])
        
        return groups
    
    def _remove_single_moving_watermark(self, file_path, watermark_group):
        """Remove a single watermark that moves position"""
        self.main_window.log_message(f"🎯 Removing moving watermark (found in {len(watermark_group)} positions)")
        
        # Calculate average position and create a larger removal area
        avg_x = sum(w['x'] for w in watermark_group) / len(watermark_group)
        avg_y = sum(w['y'] for w in watermark_group) / len(watermark_group)
        max_w = max(w['width'] for w in watermark_group)
        max_h = max(w['height'] for w in watermark_group)
        
        # Create enlarged area to cover movement
        x_range = max(w['x'] for w in watermark_group) - min(w['x'] for w in watermark_group)
        y_range = max(w['y'] for w in watermark_group) - min(w['y'] for w in watermark_group)
        
        # Expand the removal area to cover the full movement range
        expanded_watermark = {
            'x': int(min(w['x'] for w in watermark_group) - 10),
            'y': int(min(w['y'] for w in watermark_group) - 10),
            'width': int(max_w + x_range + 20),
            'height': int(max_h + y_range + 20),
            'confidence': max(w['confidence'] for w in watermark_group),
            'type': 'moving_watermark',
            'corner': 'moving_area'
        }
        
        self.main_window.log_message(f"📏 Expanded removal area: {expanded_watermark['width']}x{expanded_watermark['height']} to cover movement")
        
        # Use inpainting method for moving watermarks (works better than delogo)
        method_choice = "Smart inpaint (recommended for text)"
        method_type = "inpaint"
        output_path = file_path.rsplit(".", 1)[0] + f"_moving_watermark_removed.mp4"
        
        self.main_window.start_operation("Removing Moving Watermark")
        
        # Create and start worker thread
        self.main_window.worker_thread = WorkerThread("remove_logo", self.ffmpeg_path, file_path, 
                                                     method_type, expanded_watermark, output_path)
        self.main_window.worker_thread.progress.connect(self.main_window.log_message)
        self.main_window.worker_thread.finished.connect(self.main_window.finish_operation)
        self.main_window.worker_thread.start()
    
    def _remove_multiple_watermarks(self, file_path, watermark_groups):
        """Remove multiple watermarks sequentially - enhanced implementation"""
        self.main_window.log_message(f"🎯 Removing {len(watermark_groups)} different watermarks")
        
        # Create a combined removal area that covers all watermarks
        all_watermarks = []
        for group in watermark_groups:
            # For each group, take the most confident watermark
            best_watermark = max(group, key=lambda w: w['confidence'])
            all_watermarks.append(best_watermark)
        
        # Sort by confidence (highest first)
        all_watermarks.sort(key=lambda w: w['confidence'], reverse=True)
        
        self.main_window.log_message(f"📋 Watermarks to remove:")
        for i, watermark in enumerate(all_watermarks):
            text = watermark.get('text', 'unknown')[:20] + ('...' if len(watermark.get('text', '')) > 20 else '')
            self.main_window.log_message(f"  {i+1}. '{text}' at ({watermark['x']}, {watermark['y']}) conf: {watermark['confidence']:.3f}")
        
        # Strategy: Create a combined filter that removes all watermarks in one pass
        if len(all_watermarks) <= 3:
            # For small numbers of watermarks, use combined removal
            self._remove_combined_watermarks(file_path, all_watermarks)
        else:
            # For many watermarks, remove the most confident one first
            self.main_window.log_message(f"🎯 Too many watermarks ({len(all_watermarks)}), removing highest confidence first")
            self._remove_single_watermark(file_path, all_watermarks[0])
    
    def _remove_combined_watermarks(self, file_path, watermarks):
        """Remove multiple watermarks in a single pass using combined filters"""
        self.main_window.log_message(f"🎯 Removing {len(watermarks)} watermarks in combined operation")
        
        # Create a combined watermark that covers all areas
        min_x = min(w['x'] for w in watermarks)
        min_y = min(w['y'] for w in watermarks)
        max_x = max(w['x'] + w['width'] for w in watermarks)
        max_y = max(w['y'] + w['height'] for w in watermarks)
        
        # Add padding for better results
        padding = 10
        min_x = max(0, min_x - padding)
        min_y = max(0, min_y - padding)
        combined_width = max_x - min_x + padding
        combined_height = max_y - min_y + padding
        
        # Create a combined watermark object
        combined_watermark = {
            'x': min_x,
            'y': min_y,
            'width': combined_width,
            'height': combined_height,
            'confidence': max(w['confidence'] for w in watermarks),
            'type': 'combined_watermarks',
            'corner': 'multiple_areas',
            'watermark_count': len(watermarks)
        }
        
        self.main_window.log_message(f"📏 Combined removal area: ({min_x}, {min_y}) {combined_width}x{combined_height}")
        
        # Use inpainting method for combined removal
        method_type = "inpaint"
        output_path = file_path.rsplit(".", 1)[0] + f"_combined_watermarks_removed.mp4"
        
        self.main_window.start_operation("Removing Combined Watermarks")
        
        # Create and start worker thread
        self.main_window.worker_thread = WorkerThread("remove_logo", self.ffmpeg_path, file_path, 
                                                     method_type, combined_watermark, output_path)
        self.main_window.worker_thread.progress.connect(self.main_window.log_message)
        self.main_window.worker_thread.finished.connect(self.main_window.finish_operation)
        self.main_window.worker_thread.start()
    
    def _remove_logo_manual(self, file_path):
        """Remove logo using manual positioning (original method)"""
        # Let user choose logo removal method
        method_choice = self._get_logo_removal_method_choice()
        if not method_choice:
            return

        # Get logo position from user
        logo_position = self._get_logo_position()
        if logo_position is None:
            return

        # Map choice to processing method
        method_type = self._get_logo_removal_method(method_choice)
        output_path = file_path.rsplit(".", 1)[0] + f"_logo_removed_manual.mp4"
        
        self.main_window.start_operation(f"Removing Logo ({method_choice})")
        
        # Create and start worker thread
        self.main_window.worker_thread = WorkerThread("remove_logo", self.ffmpeg_path, file_path, 
                                                     method_type, logo_position, output_path)
        self.main_window.worker_thread.progress.connect(self.main_window.log_message)
        self.main_window.worker_thread.finished.connect(self.main_window.finish_operation)
        self.main_window.worker_thread.start()
    
    def _get_logo_removal_method_choice(self):
        """Get logo removal method from user"""
        logo_options = [
            "Blur logo area",
            "Black out logo area", 
            "Pixelate logo area",
            "Smart inpaint (recommended for text)",
            "Remove with delogo filter",
            "🎨 Lama-Cleaner (AI inpainting - best quality)"
        ]
        
        method_choice, ok = QInputDialog.getItem(self.main_window, "Select Logo Removal Method", 
                                               "Choose how to handle the logo:", 
                                               logo_options, 3, False)  # Default to inpaint
        if not ok:
            self.main_window.log_message("Logo removal operation cancelled.")
            return None
        return method_choice

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
            "1 minute (60 seconds)",
            "2 minutes (120 seconds)",
            "3 minutes (180 seconds)",
            "5 minutes (300 seconds)",
            "10 minutes (600 seconds)", 
            "15 minutes (900 seconds)",
            "20 minutes (1200 seconds)",
            "30 minutes (1800 seconds)",
            "Custom duration"
        ]
        
        duration_choice, ok = QInputDialog.getItem(self.main_window, "Select Split Duration", 
                                                  "Choose how long each part should be:", 
                                                  duration_options, 3, False)  # Default to 5 minutes
        if not ok:
            self.main_window.log_message("Split operation cancelled.")
            return None, None

        # Get the duration in seconds
        duration_map = {
            "1 minute (60 seconds)": (60, "1min"),
            "2 minutes (120 seconds)": (120, "2min"),
            "3 minutes (180 seconds)": (180, "3min"),
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
            while True:  # Loop until valid input or cancel
                custom_input, ok = QInputDialog.getText(
                    self.main_window, 
                    "Custom Duration", 
                    "Enter duration in minutes:\n"
                    "Examples: 1 (1 minute), 2.5 (2 min 30 sec), 0.5 (30 seconds)\n"
                    "Range: 0.1 to 180 minutes",
                    text=""  # Empty default so user sees their input clearly
                )
                if not ok:
                    self.main_window.log_message("Split operation cancelled.")
                    return None, None
                
                # Check if input is empty
                if not custom_input.strip():
                    self.main_window.show_error("Please enter a duration value.")
                    continue
                
                try:
                    custom_minutes = float(custom_input.strip())
                    
                    # Validate input range
                    if custom_minutes < 0.1:
                        self.main_window.show_error("Duration must be at least 0.1 minutes (6 seconds).")
                        continue
                    elif custom_minutes > 180:
                        self.main_window.show_error("Duration cannot exceed 180 minutes (3 hours).")
                        continue
                    
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
                    self.main_window.show_error("Invalid input. Please enter a valid number (e.g., 1, 2.5, 0.5).")
                    continue  # Ask for input again

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

    def _get_logo_position(self):
        """Get logo position and size from user"""
        # Ask for logo position
        position_options = [
            "Top-left corner",
            "Top-right corner",
            "Bottom-left corner", 
            "Bottom-right corner",
            "Custom position"
        ]
        
        position_choice, ok = QInputDialog.getItem(self.main_window, "Select Logo Position", 
                                                 "Where is the logo located?", 
                                                 position_options, 0, False)
        if not ok:
            self.main_window.log_message("Logo removal cancelled.")
            return None

        if position_choice == "Custom position":
            # Get custom coordinates
            coords_text, ok = QInputDialog.getText(
                self.main_window,
                "Custom Logo Position",
                "Enter logo position and size:\n"
                "Format: x,y,width,height (in pixels)\n"
                "Example: 10,10,100,50 (x=10, y=10, width=100, height=50)",
                text="10,10,100,50"
            )
            if not ok:
                return None
            
            try:
                coords = [int(x.strip()) for x in coords_text.split(",")]
                if len(coords) != 4:
                    self.main_window.show_error("Please enter exactly 4 values: x,y,width,height")
                    return None
                return {"x": coords[0], "y": coords[1], "width": coords[2], "height": coords[3]}
            except ValueError:
                self.main_window.show_error("Invalid coordinates. Please enter numbers only.")
                return None
        else:
            # Get size for predefined positions
            size_text, ok = QInputDialog.getText(
                self.main_window,
                "Logo Size",
                "Enter logo size:\n"
                "Format: width,height (in pixels)\n"
                "Example: 100,50",
                text="100,50"
            )
            if not ok:
                return None
            
            try:
                size = [int(x.strip()) for x in size_text.split(",")]
                if len(size) != 2:
                    self.main_window.show_error("Please enter exactly 2 values: width,height")
                    return None
                
                # Calculate position based on choice
                position_map = {
                    "Top-left corner": {"x": 10, "y": 10},
                    "Top-right corner": {"x": f"main_w-{size[0]}-10", "y": 10},
                    "Bottom-left corner": {"x": 10, "y": f"main_h-{size[1]}-10"},
                    "Bottom-right corner": {"x": f"main_w-{size[0]}-10", "y": f"main_h-{size[1]}-10"}
                }
                
                pos = position_map[position_choice]
                return {"x": pos["x"], "y": pos["y"], "width": size[0], "height": size[1]}
                
            except ValueError:
                self.main_window.show_error("Invalid size. Please enter numbers only.")
                return None

    def _get_logo_removal_method(self, method_choice):
        """Get the FFmpeg filter for logo removal method"""
        method_map = {
            "Blur logo area": "blur",
            "Black out logo area": "blackout",
            "Pixelate logo area": "pixelate", 
            "Smart inpaint (recommended for text)": "inpaint",
            "Remove with delogo filter": "delogo",
            "🎨 Lama-Cleaner (AI inpainting - best quality)": "lama"
        }
        return method_map.get(method_choice, "inpaint")  # Default to inpaint for text
    
    def _remove_timeline_watermarks(self, file_path, watermark_timelines):
        """Remove watermarks using timeline-based analysis for precise removal"""
        
        if len(watermark_timelines) == 1:
            # Single watermark - use optimal removal method
            timeline = watermark_timelines[0]
            self._remove_single_timeline_watermark(file_path, timeline)
        else:
            # Multiple watermarks - select the best candidate
            self.main_window.log_message(f"🎯 Processing {len(watermark_timelines)} different watermarks")
            
            # Sort by priority: watermark indicators, confidence, and number of detections
            sorted_timelines = sorted(watermark_timelines, 
                                    key=lambda t: (
                                        t.get('is_watermark', False),  # Prioritize actual watermarks
                                        t.get('confidence', 0),        # Then by confidence
                                        len(t.get('positions', []))    # Then by consistency
                                    ), reverse=True)
            
            # Show user what we're targeting
            best_timeline = sorted_timelines[0]
            text = best_timeline.get('text', 'Unknown')[:30]
            confidence = best_timeline.get('confidence', 0)
            is_watermark = best_timeline.get('is_watermark', False)
            
            watermark_type = "watermark" if is_watermark else "text element"
            self.main_window.log_message(f"🎯 Targeting best {watermark_type}: '{text}' (confidence: {confidence:.2f})")
            
            # Remove the best candidate first
            self._remove_single_timeline_watermark(file_path, best_timeline)
    
    def _remove_single_timeline_watermark(self, file_path, watermark_timeline):
        """Remove a single watermark using its timeline information"""
        
        text = watermark_timeline.get('text', 'Unknown')[:30]
        is_moving = watermark_timeline.get('is_moving', False)
        positions = watermark_timeline.get('positions', [])
        confidence = watermark_timeline.get('confidence', 0)
        
        self.main_window.log_message(f"🎯 Removing watermark: '{text}' (confidence: {confidence:.2f})")
        
        if is_moving and len(positions) > 1:
            # Moving watermark - use dynamic removal
            self._remove_moving_timeline_watermark(file_path, watermark_timeline)
        else:
            # Static watermark - use traditional removal
            self._remove_static_timeline_watermark(file_path, watermark_timeline)
    
    def _remove_moving_timeline_watermark(self, file_path, watermark_timeline):
        """Remove a moving watermark using time-based FFmpeg filters"""
        
        text = watermark_timeline.get('text', 'Unknown')[:20]
        positions = watermark_timeline.get('positions', [])
        
        self.main_window.log_message(f"🎬 Removing moving watermark '{text}' across {len(positions)} positions")
        
        # Import the logo detector for dynamic command generation
        try:
            from logo_detector import LogoDetector
            detector = LogoDetector(self.ffmpeg_path)
            
            # Generate dynamic removal command
            dynamic_cmd = detector.create_dynamic_removal_command(file_path, watermark_timeline, method='blur')
            
            if dynamic_cmd:
                self.main_window.log_message("🎯 Using dynamic time-based removal with FFmpeg")
                
                output_path = file_path.rsplit(".", 1)[0] + f"_moving_removed.mp4"
                
                self.main_window.start_operation("Removing Moving Watermark (Dynamic)")
                
                # Create and start worker thread with dynamic command
                self.main_window.worker_thread = WorkerThread("dynamic_removal", dynamic_cmd, output_path)
                self.main_window.worker_thread.progress.connect(self.main_window.log_message)
                self.main_window.worker_thread.finished.connect(self.main_window.finish_operation)
                self.main_window.worker_thread.start()
                
                return
            else:
                self.main_window.log_message("⚠️ Dynamic removal failed, falling back to expanded area method")
                
        except Exception as e:
            self.main_window.log_message(f"⚠️ Dynamic removal error: {e}, using fallback method")
        
        # Fallback to expanded area method
        self._remove_moving_timeline_watermark_fallback(file_path, watermark_timeline)
    
    def _remove_moving_timeline_watermark_fallback(self, file_path, watermark_timeline):
        """Fallback method for moving watermarks using expanded area"""
        
        positions = watermark_timeline.get('positions', [])
        text = watermark_timeline.get('text', 'Unknown')[:20]
        
        self.main_window.log_message(f"🎯 Using expanded area method for moving watermark '{text}'")
        
        # Calculate expanded area covering all positions
        min_x = min(p['x'] for p in positions)
        min_y = min(p['y'] for p in positions)
        max_x = max(p['x'] + p['width'] for p in positions)
        max_y = max(p['y'] + p['height'] for p in positions)
        
        # Add padding for better coverage
        padding = 15
        raw_x = max(0, min_x - padding)
        raw_y = max(0, min_y - padding)
        raw_w = max_x - min_x + (2 * padding)
        raw_h = max_y - min_y + (2 * padding)
        
        # Get video dimensions for coordinate validation
        video_width, video_height = self._get_video_dimensions(file_path)
        
        # Validate and fix coordinates
        x, y, w, h = self._validate_coordinates(raw_x, raw_y, raw_w, raw_h, video_width, video_height)
        
        expanded_watermark = {
            'x': x,
            'y': y,
            'width': w,
            'height': h,
            'confidence': watermark_timeline.get('confidence', 0),
            'type': 'moving_watermark',
            'text': text
        }
        
        self.main_window.log_message(f"📏 Expanded area: ({x}, {y}) {w}x{h} (validated)")
        
        # Use inpainting method for better results on moving watermarks
        method_type = "inpaint"
        output_path = file_path.rsplit(".", 1)[0] + f"_moving_removed.mp4"
        
        self.main_window.start_operation("Removing Moving Watermark (Expanded Area)")
        
        # Create and start worker thread
        self.main_window.worker_thread = WorkerThread("remove_logo", self.ffmpeg_path, file_path, 
                                                     method_type, expanded_watermark, output_path)
        self.main_window.worker_thread.progress.connect(self.main_window.log_message)
        self.main_window.worker_thread.finished.connect(self.main_window.finish_operation)
        self.main_window.worker_thread.start()
    
    def _remove_static_timeline_watermark(self, file_path, watermark_timeline):
        """Remove a static watermark using its timeline information"""
        
        positions = watermark_timeline.get('positions', [])
        text = watermark_timeline.get('text', 'Unknown')[:30]
        
        if not positions:
            self.main_window.log_message("❌ No position data available for static watermark")
            return
            
        # Use the most confident position
        best_position = max(positions, key=lambda p: p.get('confidence', 0))
        
        # Get video dimensions for coordinate validation
        video_width, video_height = self._get_video_dimensions(file_path)
        
        # Validate and fix coordinates
        x, y, w, h = self._validate_coordinates(
            best_position['x'], best_position['y'], 
            best_position['width'], best_position['height'],
            video_width, video_height
        )
        
        # Convert to legacy format for compatibility with validated coordinates
        legacy_watermark = {
            'x': x,
            'y': y,
            'width': w,
            'height': h,
            'confidence': best_position.get('confidence', 0),
            'type': 'static_watermark',
            'text': text
        }
        
        self.main_window.log_message(f"📍 Removing static watermark '{text}' at ({x}, {y}) size {w}x{h}")
        
        # Choose optimal removal method - prefer delogo for better results
        if watermark_timeline.get('is_watermark', False) or any(indicator in text.lower() for indicator in ['www', '.com', '©', '®', '™']):
            method_type = "delogo"
            method_choice = "Remove with delogo filter"
        elif 'text' in text.lower() or len(text) > 5:
            method_type = "inpaint"
            method_choice = "Smart inpaint (recommended for text)"
        else:
            method_type = "blur"
            method_choice = "Blur logo area"
        
        output_path = file_path.rsplit(".", 1)[0] + f"_static_removed.mp4"
        
        self.main_window.start_operation(f"Removing Static Watermark ({method_choice})")
        
        # Create and start worker thread
        self.main_window.worker_thread = WorkerThread("remove_logo", self.ffmpeg_path, file_path, 
                                                     method_type, legacy_watermark, output_path)
        self.main_window.worker_thread.progress.connect(self.main_window.log_message)
        self.main_window.worker_thread.finished.connect(self.main_window.finish_operation)
        self.main_window.worker_thread.start()
    
    def _validate_coordinates(self, x, y, w, h, video_width, video_height):
        """Validate and fix coordinates to ensure they're within video boundaries"""
        # Ensure coordinates are within bounds
        x = max(0, min(x, video_width - 1))
        y = max(0, min(y, video_height - 1))
        
        # Ensure dimensions don't exceed frame boundaries
        max_w = video_width - x
        max_h = video_height - y
        w = min(w, max_w - 1)  # Leave 1 pixel margin to avoid boundary issues
        h = min(h, max_h - 1)  # Leave 1 pixel margin to avoid boundary issues
        
        # Ensure minimum size for FFmpeg filters
        w = max(w, 2)
        h = max(h, 2)
        
        return x, y, w, h
    
    def _get_video_dimensions(self, video_path):
        """Get video dimensions using ffprobe"""
        try:
            probe_cmd = [
                "ffprobe", "-v", "error", "-select_streams", "v:0", 
                "-show_entries", "stream=width,height", "-of", "csv=p=0", video_path
            ]
            probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
            if probe_result.returncode == 0:
                dimensions = probe_result.stdout.strip().split(',')
                return int(dimensions[0]), int(dimensions[1])
        except:
            pass
        return 1920, 1080  # Default fallback
