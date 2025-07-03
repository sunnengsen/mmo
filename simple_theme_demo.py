#!/usr/bin/env python3
"""
Simple responsive theme switching demo
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QTextEdit
)
from PyQt6.QtCore import Qt

from ui_styles_new import (
    get_app_style, toggle_theme, get_current_theme
)


class SimpleThemeDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎨 Simple Theme Switcher")
        self.setGeometry(100, 100, 600, 400)
        self.setup_ui()
        self.apply_theme()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        self.title = QLabel("🎨 Theme Switching Demo")
        self.title.setObjectName("title")
        layout.addWidget(self.title)
        
        # Current theme display
        self.theme_display = QLabel(f"Current Theme: {get_current_theme()}")
        self.theme_display.setObjectName("label")
        layout.addWidget(self.theme_display)
        
        # Theme toggle button
        self.toggle_btn = QPushButton("🌙 Switch to Dark Mode")
        self.toggle_btn.setObjectName("primary_btn")
        self.toggle_btn.clicked.connect(self.on_toggle_theme)
        layout.addWidget(self.toggle_btn)
        
        # Test input
        from PyQt6.QtWidgets import QLineEdit
        self.test_input = QLineEdit()
        self.test_input.setPlaceholderText("Type something to test input styling...")
        self.test_input.setObjectName("input")
        layout.addWidget(self.test_input)
        
        # Test log
        self.log = QTextEdit()
        self.log.setObjectName("log")
        self.log.setMaximumHeight(150)
        self.log.setPlainText("Theme demo initialized\nClick the button to switch themes")
        layout.addWidget(self.log)
        
    def on_toggle_theme(self):
        """Handle theme toggle button click"""
        print("Toggle button clicked!")  # Debug
        
        # Toggle theme
        new_theme = toggle_theme()
        print(f"New theme: {new_theme}")  # Debug
        
        # Update display
        self.theme_display.setText(f"Current Theme: {new_theme}")
        
        # Update button text
        if new_theme == "dark":
            self.toggle_btn.setText("☀️ Switch to Light Mode")
        else:
            self.toggle_btn.setText("🌙 Switch to Dark Mode")
        
        # Apply new theme
        self.apply_theme()
        
        # Log the change
        self.log.append(f"Switched to {new_theme} theme!")
        
    def apply_theme(self):
        """Apply current theme"""
        try:
            style = get_app_style()
            self.setStyleSheet(style)
            print(f"Applied {get_current_theme()} theme")
        except Exception as e:
            print(f"Error applying theme: {e}")


def main():
    app = QApplication(sys.argv)
    
    demo = SimpleThemeDemo()
    demo.show()
    
    print("Simple theme demo started!")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
