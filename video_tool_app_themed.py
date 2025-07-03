#!/usr/bin/env python3
"""
Complete integration example for adding theme switching to video_tool_app.py
This shows exactly how to modify your existing application.
"""

import sys
import shutil
import time
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QTextEdit, QLabel, QFileDialog, QMessageBox, QInputDialog,
    QFrame, QScrollArea, QGroupBox, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer

# UPDATED IMPORT - Replace the old import with this:
from ui_styles_new import (
    get_app_style, toggle_theme, get_current_theme, 
    get_status_colors, theme_manager
)

# Import your existing modules (unchanged)
from video_operations import VideoOperations


class VideoToolAppWithThemes(QWidget):
    """Enhanced Video Tool App with theme switching"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎬 Video Tool Pro - yt-dlp + ffmpeg")
        self.setMinimumSize(800, 950)
        
        # Initialize variables
        self.download_folder = None
        self.worker_thread = None
        self.start_time = None
        
        # Initialize video operations handler
        self.video_ops = VideoOperations(self)
        
        # Setup UI and styling
        self.setup_ui()
        self.apply_theme()  # CHANGED: Use apply_theme instead of setup_styling
        
        # Timer for elapsed time display
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_elapsed_time)

        # Detect executables
        self.ffmpeg_path = shutil.which("ffmpeg")
        self.ytdlp_path = shutil.which("yt-dlp")

        if not self.ffmpeg_path:
            self.show_error("ffmpeg not found. Please install ffmpeg and make sure it is in your PATH.")
        if not self.ytdlp_path:
            self.show_error("yt-dlp not found. Please install yt-dlp and make sure it is in your PATH.")

    def setup_ui(self):
        """Setup the user interface"""
        main_layout = QVBoxLayout(self)
        
        # NEW: Add header with theme button
        self._create_header(main_layout)
        
        # Your existing sections (unchanged)
        self._create_download_section(main_layout)
        self._create_processing_section(main_layout)
        self._create_progress_section(main_layout)
        self._create_log_section(main_layout)

    def _create_header(self, main_layout):
        """NEW: Create header with theme toggle button"""
        header_layout = QHBoxLayout()
        
        # Title (moved from individual sections)
        title = QLabel("🎬 Video Tool Pro")
        title.setObjectName("title")
        header_layout.addWidget(title)
        
        # Spacer to push theme button to the right
        header_layout.addStretch()
        
        # Theme toggle button
        self.theme_btn = QPushButton("🌙 Dark Mode")
        self.theme_btn.setObjectName("theme_btn")
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.theme_btn.setMinimumWidth(140)
        header_layout.addWidget(self.theme_btn)
        
        main_layout.addLayout(header_layout)

    # NEW: Theme-related methods
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        new_theme = toggle_theme()
        self.apply_theme()
        
        # Update theme button text
        if new_theme == "dark":
            self.theme_btn.setText("☀️ Light Mode")
        else:
            self.theme_btn.setText("🌙 Dark Mode")
        
        # Update status colors for current status
        self.update_status_colors()
        
        # Log the theme change
        self.log.append(f"🎨 Theme switched to: {new_theme} mode")

    def apply_theme(self):
        """Apply the current theme to the application"""
        self.setStyleSheet(get_app_style())

    def update_status_colors(self):
        """Update status label colors based on current theme"""
        status_colors = get_status_colors()
        # You'll need to track your current status and apply appropriate color
        # For example, if currently showing "ready" status:
        self.status_label.setStyleSheet(status_colors.get("ready", ""))

    # UPDATED: Status methods to use dynamic colors
    def update_status(self, message, status_type="ready"):
        """Update status with theme-aware colors"""
        self.status_label.setText(message)
        status_colors = get_status_colors()
        self.status_label.setStyleSheet(status_colors.get(status_type, ""))

    # Your existing methods remain the same, just update status calls:
    def _create_download_section(self, main_layout):
        """Create video download section"""
        download_group = QGroupBox("📥 Video Download")
        download_group.setObjectName("group")
        download_layout = QVBoxLayout()

        self.url_label = QLabel("🔗 Video URL:")
        self.url_label.setObjectName("label")
        download_layout.addWidget(self.url_label)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste YouTube, TikTok, or other video URL here...")
        self.url_input.setObjectName("input")
        download_layout.addWidget(self.url_input)

        # Folder selection row
        folder_row = QHBoxLayout()
        self.select_folder_btn = QPushButton("📁 Select Download Folder")
        self.select_folder_btn.setObjectName("primary_btn")
        self.select_folder_btn.clicked.connect(self.select_download_folder)
        folder_row.addWidget(self.select_folder_btn)

        self.download_btn = QPushButton("⬇️ Download Video")
        self.download_btn.setObjectName("success_btn")
        self.download_btn.clicked.connect(self.download_video)  # You'll need to implement this
        folder_row.addWidget(self.download_btn)

        download_layout.addLayout(folder_row)

        self.folder_label = QLabel("📂 No folder selected. Default: Current Folder")
        self.folder_label.setObjectName("info_label")
        download_layout.addWidget(self.folder_label)

        download_group.setLayout(download_layout)
        main_layout.addWidget(download_group)

    def _create_processing_section(self, main_layout):
        """Create video processing section"""
        processing_group = QGroupBox("⚙️ Video Processing")
        processing_group.setObjectName("group")
        processing_layout = QVBoxLayout()

        # First row of buttons
        row1 = QHBoxLayout()
        self.flip_btn = QPushButton("🔄 Flip Video")
        self.flip_btn.setObjectName("primary_btn")
        row1.addWidget(self.flip_btn)

        self.split_btn = QPushButton("✂️ Split Video")
        self.split_btn.setObjectName("primary_btn")
        row1.addWidget(self.split_btn)

        processing_layout.addLayout(row1)

        # Second row of buttons
        row2 = QHBoxLayout()
        self.flip_folder_btn = QPushButton("🔄 Flip Folder Videos")
        self.flip_folder_btn.setObjectName("secondary_btn")
        row2.addWidget(self.flip_folder_btn)

        self.convert_to_reel_btn = QPushButton("📱 Convert to TikTok/Reel")
        self.convert_to_reel_btn.setObjectName("accent_btn")
        row2.addWidget(self.convert_to_reel_btn)

        processing_layout.addLayout(row2)
        processing_group.setLayout(processing_layout)
        main_layout.addWidget(processing_group)

    def _create_progress_section(self, main_layout):
        """Create progress tracking section"""
        progress_group = QGroupBox("📊 Progress Status")
        progress_group.setObjectName("group")
        progress_layout = QVBoxLayout()

        # Status row
        status_row = QHBoxLayout()
        self.status_label = QLabel("⏱️ Ready")
        self.status_label.setObjectName("status_label")
        status_row.addWidget(self.status_label)

        self.elapsed_label = QLabel("Duration: 00:00")
        self.elapsed_label.setObjectName("elapsed_label")
        status_row.addWidget(self.elapsed_label)
        status_row.addStretch()

        progress_layout.addLayout(status_row)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)

        progress_group.setLayout(progress_layout)
        main_layout.addWidget(progress_group)

    def _create_log_section(self, main_layout):
        """Create activity log section"""
        log_group = QGroupBox("📋 Activity Log")
        log_group.setObjectName("group")
        log_layout = QVBoxLayout()

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setObjectName("log")
        self.log.setMaximumHeight(300)
        log_layout.addWidget(self.log)

        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)

    def update_elapsed_time(self):
        """Update the elapsed time display"""
        if self.start_time:
            elapsed = time.time() - self.start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            self.elapsed_label.setText(f"Duration: {minutes:02d}:{seconds:02d}")

    # Placeholder methods - replace with your existing implementations
    def select_download_folder(self):
        """Select download folder"""
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if folder:
            self.download_folder = folder
            self.folder_label.setText(f"📂 {folder}")

    def download_video(self):
        """Download video - placeholder"""
        self.update_status("🔄 Downloading...", "working")
        self.log.append("Download started...")

    def show_error(self, message):
        """Show error message"""
        QMessageBox.critical(self, "Error", message)


def main():
    """Main function"""
    app = QApplication(sys.argv)
    
    # Create and show the application
    window = VideoToolAppWithThemes()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
