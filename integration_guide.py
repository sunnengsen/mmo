"""
Integration guide for adding theme switching to video_tool_app.py

This file shows the changes needed to integrate theme switching into your existing application.
"""

# STEP 1: Update imports at the top of video_tool_app.py
# Replace this line:
# from ui_styles import APP_STYLE, STATUS_COLORS

# With these lines:
from ui_styles_new import (
    get_app_style, toggle_theme, get_current_theme, 
    get_status_colors, theme_manager
)

# STEP 2: Add theme button to your UI setup
# In your setup_ui method, add this to create a theme toggle button:

def add_theme_button_to_header(self):
    """Add this method to your VideoToolApp class"""
    # Create a header layout if you don't have one
    header_layout = QHBoxLayout()
    
    # Your existing title
    title = QLabel("🎬 Video Tool Pro - yt-dlp + ffmpeg")
    title.setObjectName("title")
    header_layout.addWidget(title)
    
    # Add theme toggle button
    self.theme_btn = QPushButton("🌙 Dark Mode")
    self.theme_btn.setObjectName("theme_btn")
    self.theme_btn.clicked.connect(self.toggle_theme)
    header_layout.addWidget(self.theme_btn)
    
    # Add this layout to your main layout
    # main_layout.addLayout(header_layout)

# STEP 3: Replace the setup_styling method
# Replace your existing setup_styling method with this:

def setup_styling(self):
    """Apply CSS styling with theme support"""
    self.setStyleSheet(get_app_style())

# STEP 4: Add theme toggle method
# Add this new method to your VideoToolApp class:

def toggle_theme(self):
    """Toggle between light and dark themes"""
    new_theme = toggle_theme()
    self.apply_theme()
    
    # Update theme button text
    if new_theme == "dark":
        self.theme_btn.setText("☀️ Light Mode")
    else:
        self.theme_btn.setText("🌙 Dark Mode")
        
    # Update status colors
    self.update_status_colors()
    
    # Log the theme change
    self.log.append(f"Theme switched to: {new_theme} mode")

def apply_theme(self):
    """Apply the current theme to the application"""
    self.setStyleSheet(get_app_style())

def update_status_colors(self):
    """Update status label colors based on current theme"""
    status_colors = get_status_colors()
    # Update your status label with current theme colors
    current_status = "ready"  # or whatever your current status is
    self.status_label.setStyleSheet(status_colors[current_status])

# STEP 5: Update status color usage throughout your app
# Wherever you currently use STATUS_COLORS, replace it with get_status_colors()
# For example:
# OLD: self.status_label.setStyleSheet(STATUS_COLORS["ready"])
# NEW: self.status_label.setStyleSheet(get_status_colors()["ready"])

# STEP 6: Initialize theme button text in __init__
# Add this to your __init__ method after setup_ui():
def init_theme_button(self):
    """Initialize theme button text based on current theme"""
    if get_current_theme() == "dark":
        self.theme_btn.setText("☀️ Light Mode")
    else:
        self.theme_btn.setText("🌙 Dark Mode")

"""
COMPLETE EXAMPLE: Here's how your modified VideoToolApp class would look:
"""

class VideoToolApp(QWidget):
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
        self.setup_styling()
        self.init_theme_button()  # NEW: Initialize theme button
        
        # Rest of your existing initialization...
    
    def setup_ui(self):
        """Setup the user interface"""
        main_layout = QVBoxLayout(self)
        
        # NEW: Add header with theme button
        self._create_header(main_layout)
        
        # Your existing sections...
        self._create_download_section(main_layout)
        self._create_processing_section(main_layout)
        self._create_progress_section(main_layout)
        self._create_log_section(main_layout)
    
    def _create_header(self, main_layout):
        """Create header with theme toggle button"""
        header_layout = QHBoxLayout()
        
        title = QLabel("🎬 Video Tool Pro - yt-dlp + ffmpeg")
        title.setObjectName("title")
        header_layout.addWidget(title)
        
        self.theme_btn = QPushButton("🌙 Dark Mode")
        self.theme_btn.setObjectName("theme_btn")
        self.theme_btn.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_btn)
        
        main_layout.addLayout(header_layout)
    
    def setup_styling(self):
        """Apply CSS styling with theme support"""
        self.setStyleSheet(get_app_style())
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        new_theme = toggle_theme()
        self.apply_theme()
        
        if new_theme == "dark":
            self.theme_btn.setText("☀️ Light Mode")
        else:
            self.theme_btn.setText("🌙 Dark Mode")
            
        self.update_status_colors()
        self.log.append(f"Theme switched to: {new_theme} mode")
    
    def apply_theme(self):
        """Apply the current theme to the application"""
        self.setStyleSheet(get_app_style())
    
    def update_status_colors(self):
        """Update status label colors based on current theme"""
        status_colors = get_status_colors()
        # Update status label with current theme colors
        # You'll need to track your current status state
        self.status_label.setStyleSheet(status_colors.get("ready", ""))
    
    def init_theme_button(self):
        """Initialize theme button text based on current theme"""
        if get_current_theme() == "dark":
            self.theme_btn.setText("☀️ Light Mode")
        else:
            self.theme_btn.setText("🌙 Dark Mode")

    # All your existing methods remain the same...
