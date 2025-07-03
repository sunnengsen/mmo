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

# Import enhanced UI with theme switching
from ui_styles_new import (
    get_app_style, toggle_theme, get_current_theme, 
    get_status_colors, theme_manager
)
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
        self.apply_theme()
        
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
        """Setup the user interface with theme switching"""
        main_layout = QVBoxLayout()
        
        # Theme switching button at the top
        self._create_theme_section(main_layout)
        
        # Original sections
        self._create_download_section(main_layout)
        self._create_processing_section(main_layout)
        self._create_progress_section(main_layout)
        self._create_log_section(main_layout)
        
        self.setLayout(main_layout)

    def _create_theme_section(self, main_layout):
        """Create theme switching section"""
        theme_group = QGroupBox("🎨 Theme Settings")
        theme_group.setObjectName("group")
        theme_layout = QHBoxLayout()
        
        current_theme = get_current_theme()
        self.theme_btn = QPushButton(f"🌙 Switch to {'Light' if current_theme == 'dark' else 'Dark'} Mode")
        self.theme_btn.setObjectName("accent_btn")
        self.theme_btn.clicked.connect(self.toggle_theme)
        theme_layout.addWidget(self.theme_btn)
        
        # Theme info label
        self.theme_info = QLabel(f"Current theme: {current_theme.title()}")
        self.theme_info.setObjectName("info_label")
        theme_layout.addWidget(self.theme_info)
        theme_layout.addStretch()
        
        theme_group.setLayout(theme_layout)
        main_layout.addWidget(theme_group)

    def _create_download_section(self, main_layout):
        """Create download section"""
        download_group = QGroupBox("⬇️ Download Video")
        download_group.setObjectName("group")
        download_layout = QVBoxLayout()

        self.url_label = QLabel("📎 Video URL:")
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
        self.download_btn.clicked.connect(self.video_ops.download_video)
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
        self.flip_btn.clicked.connect(self.video_ops.flip_video)
        row1.addWidget(self.flip_btn)

        self.split_btn = QPushButton("✂️ Split Video")
        self.split_btn.setObjectName("primary_btn")
        self.split_btn.clicked.connect(self.video_ops.split_video)
        row1.addWidget(self.split_btn)

        processing_layout.addLayout(row1)

        # Second row of buttons
        row2 = QHBoxLayout()
        self.flip_folder_btn = QPushButton("🔄 Flip Folder Videos")
        self.flip_folder_btn.setObjectName("secondary_btn")
        self.flip_folder_btn.clicked.connect(self.video_ops.flip_folder_videos)
        row2.addWidget(self.flip_folder_btn)

        self.convert_to_reel_btn = QPushButton("📱 Convert to TikTok/Reel")
        self.convert_to_reel_btn.setObjectName("accent_btn")
        self.convert_to_reel_btn.clicked.connect(self.video_ops.convert_to_reel)
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

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        new_theme = toggle_theme()
        self.apply_theme()
        
        # Update button text
        self.theme_btn.setText(f"🌙 Switch to {'Light' if new_theme == 'dark' else 'Dark'} Mode")
        self.theme_info.setText(f"Current theme: {new_theme.title()}")
        
        self.log_message(f"Theme switched to {new_theme.title()} mode")

    def apply_theme(self):
        """Apply the current theme to the application"""
        app_style = get_app_style()
        self.setStyleSheet(app_style)

    def update_elapsed_time(self):
        """Update the elapsed time display"""
        if self.start_time:
            elapsed = time.time() - self.start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            self.elapsed_label.setText(f"Duration: {minutes:02d}:{seconds:02d}")

    def start_operation(self, operation_name):
        """Start an operation with progress tracking"""
        self.start_time = time.time()
        self.timer.start(1000)  # Update every second
        status_colors = get_status_colors()
        self.status_label.setText(f"🔄 {operation_name}...")
        self.status_label.setStyleSheet(status_colors['working'])
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.set_buttons_enabled(False)

    def finish_operation(self, success, message):
        """Finish an operation and update status"""
        self.timer.stop()
        status_colors = get_status_colors()
        if success:
            self.status_label.setText("✅ Completed")
            self.status_label.setStyleSheet(status_colors['success'])
        else:
            self.status_label.setText("❌ Failed")
            self.status_label.setStyleSheet(status_colors['error'])
        
        self.progress_bar.setVisible(False)
        self.log_message(message)
        self.set_buttons_enabled(True)
        
        # Reset to ready after 3 seconds
        QTimer.singleShot(3000, self.reset_status)

    def reset_status(self):
        """Reset status to ready"""
        status_colors = get_status_colors()
        self.status_label.setText("⏱️ Ready")
        self.status_label.setStyleSheet(status_colors['ready'])

    def set_buttons_enabled(self, enabled):
        """Enable or disable all buttons"""
        self.download_btn.setEnabled(enabled)
        self.flip_btn.setEnabled(enabled)
        self.split_btn.setEnabled(enabled)
        self.flip_folder_btn.setEnabled(enabled)
        self.convert_to_reel_btn.setEnabled(enabled)
        self.select_folder_btn.setEnabled(enabled)

    def log_message(self, message):
        """Add a message to the log"""
        timestamp = time.strftime("%H:%M:%S")
        self.log.append(f"[{timestamp}] {message}")

    def select_download_folder(self):
        """Select download folder"""
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if folder:
            self.download_folder = folder
            self.folder_label.setText(f"📂 {folder}")
            self.log_message(f"Download folder set to: {folder}")

    def show_error(self, message):
        """Show error message"""
        QMessageBox.critical(self, "Error", message)
        self.log_message(f"Error: {message}")


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show window with theme switching
    window = VideoToolAppWithThemes()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
