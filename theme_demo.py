#!/usr/bin/env python3
"""
Demo application showing how to integrate theme switching with ui_styles_new.py
This demonstrates how to modify your existing video_tool_app.py to support theme switching.
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QTextEdit, QLabel, QGroupBox, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer

# Import the new theme-aware styles
from ui_styles_new import (
    get_app_style, toggle_theme, get_current_theme, 
    get_status_colors, theme_manager
)


class ThemeAwareVideoApp(QWidget):
    """Demo application with theme switching capability"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎬 Video Tool Pro - Theme Demo")
        self.setMinimumSize(800, 600)
        
        # Setup UI first
        self.setup_ui()
        
        # Apply initial theme
        self.apply_theme()
        
        # Initialize theme button text
        self.init_theme_button_text()
        
        # Center the window
        self.center_window()
        
    def center_window(self):
        """Center the window on screen"""
        qr = self.frameGeometry()
        screen = QApplication.primaryScreen()
        cp = screen.availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def setup_ui(self):
        """Setup the user interface"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header with theme toggle
        self._create_header(main_layout)
        
        # Demo sections
        self._create_demo_sections(main_layout)
        
    def _create_header(self, main_layout):
        """Create header with theme toggle button"""
        header_layout = QHBoxLayout()
        
        # Title
        title = QLabel("🎬 Video Tool Pro - Theme Demo")
        title.setObjectName("title")
        header_layout.addWidget(title)
        
        # Spacer
        header_layout.addStretch()
        
        # Theme toggle button
        self.theme_btn = QPushButton("🌙 Dark Mode")
        self.theme_btn.setObjectName("theme_btn")
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.theme_btn.setMinimumWidth(140)
        header_layout.addWidget(self.theme_btn)
        
        main_layout.addLayout(header_layout)
        
        # Subtitle
        subtitle = QLabel("Click the theme button to switch between light and dark modes")
        subtitle.setObjectName("subtitle")
        main_layout.addWidget(subtitle)
        
    def _create_demo_sections(self, main_layout):
        """Create demo sections to showcase theme switching"""
        
        # Input section
        input_group = QGroupBox("📝 Input Demo")
        input_group.setObjectName("group")
        input_layout = QVBoxLayout()
        
        input_label = QLabel("Video URL:")
        input_label.setObjectName("label")
        input_layout.addWidget(input_label)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste video URL here...")
        self.url_input.setObjectName("input")
        input_layout.addWidget(self.url_input)
        
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)
        
        # Buttons section
        buttons_group = QGroupBox("🔘 Button Demo")
        buttons_group.setObjectName("group")
        buttons_layout = QVBoxLayout()
        
        row1 = QHBoxLayout()
        primary_btn = QPushButton("Primary Button")
        primary_btn.setObjectName("primary_btn")
        row1.addWidget(primary_btn)
        
        secondary_btn = QPushButton("Secondary Button")
        secondary_btn.setObjectName("secondary_btn")
        row1.addWidget(secondary_btn)
        
        buttons_layout.addLayout(row1)
        
        row2 = QHBoxLayout()
        success_btn = QPushButton("Success Button")
        success_btn.setObjectName("success_btn")
        row2.addWidget(success_btn)
        
        accent_btn = QPushButton("Accent Button")
        accent_btn.setObjectName("accent_btn")
        row2.addWidget(accent_btn)
        
        buttons_layout.addLayout(row2)
        buttons_group.setLayout(buttons_layout)
        main_layout.addWidget(buttons_group)
        
        # Status section
        status_group = QGroupBox("📊 Status Demo")
        status_group.setObjectName("group")
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel("✅ Ready")
        self.status_label.setObjectName("status_label")
        status_layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.setValue(65)
        status_layout.addWidget(self.progress_bar)
        
        status_group.setLayout(status_layout)
        main_layout.addWidget(status_group)
        
        # Log section
        log_group = QGroupBox("📋 Log Demo")
        log_group.setObjectName("group")
        log_layout = QVBoxLayout()
        
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setObjectName("log")
        self.log.setMaximumHeight(150)
        self.log.setPlainText(
            "Theme switching demo initialized\n"
            "Click the theme button to switch between light and dark modes\n"
            "All UI elements will update automatically"
        )
        log_layout.addWidget(self.log)
        
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)
        
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        try:
            new_theme = toggle_theme()
            print(f"Toggling to {new_theme} theme...")  # Debug output
            
            # Apply the new theme
            self.apply_theme()
            
            # Update theme button text
            self.update_theme_button_text(new_theme)
            
            # Update status colors
            self.update_status_colors()
            
            # Log the theme change
            self.log.append(f"✅ Theme switched to: {new_theme} mode")
            self.log.append(f"Current theme: {get_current_theme()}")
            
            print(f"Theme switching completed successfully!")  # Debug output
            
        except Exception as e:
            print(f"Error during theme switching: {e}")
            self.log.append(f"❌ Error switching theme: {str(e)}")
    
    def update_theme_button_text(self, theme):
        """Update theme button text based on current theme"""
        if theme == "dark":
            self.theme_btn.setText("☀️ Light Mode")
        else:
            self.theme_btn.setText("🌙 Dark Mode")
    
    def init_theme_button_text(self):
        """Initialize theme button text based on current theme"""
        current_theme = get_current_theme()
        self.update_theme_button_text(current_theme)
        
    def apply_theme(self):
        """Apply the current theme to the application"""
        try:
            style = get_app_style()
            print(f"Applying style with {len(style)} characters...")  # Debug output
            self.setStyleSheet(style)
            
            # Force a repaint
            self.update()
            self.repaint()
            
        except Exception as e:
            print(f"Error applying theme: {e}")
        
    def update_status_colors(self):
        """Update status label colors based on current theme"""
        try:
            status_colors = get_status_colors()
            # Apply ready status color to demonstrate color changes
            self.status_label.setStyleSheet(status_colors["ready"])
            
            # Also update progress bar to show it's working
            current_value = self.progress_bar.value()
            new_value = (current_value + 10) % 100
            self.progress_bar.setValue(new_value)
            
        except Exception as e:
            print(f"Error updating status colors: {e}")


def main():
    """Main function to run the demo application"""
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("Video Tool Pro Theme Demo")
        
        print("Creating demo application...")
        
        # Create and show the demo window
        demo = ThemeAwareVideoApp()
        demo.show()
        demo.raise_()  # Bring window to front
        demo.activateWindow()  # Make sure it's active
        
        print("Demo application started successfully!")
        print("Current theme:", get_current_theme())
        
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
