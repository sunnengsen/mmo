"""
UI Styling constants and styles for the Video Tool Pro application.
Supports both light and dark themes with theme switching functionality.
"""

# Theme management
class ThemeManager:
    """Manages theme switching between light and dark modes"""
    
    def __init__(self):
        self.current_theme = "light"  # Default theme
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        return self.current_theme
    
    def set_theme(self, theme):
        """Set specific theme (light or dark)"""
        if theme in ["light", "dark"]:
            self.current_theme = theme
        return self.current_theme
    
    def get_current_theme(self):
        """Get current theme"""
        return self.current_theme

# Global theme manager instance
theme_manager = ThemeManager()

# Status color constants for light theme
STATUS_COLORS_LIGHT = {
    "ready": "color: #27ae60; background-color: rgba(39, 174, 96, 0.1);",
    "working": "color: #f39c12; background-color: rgba(243, 156, 18, 0.1);",
    "success": "color: #27ae60; background-color: rgba(39, 174, 96, 0.1);",
    "error": "color: #e74c3c; background-color: rgba(231, 76, 60, 0.1);"
}

# Status color constants for dark theme
STATUS_COLORS_DARK = {
    "ready": "color: #2ecc71; background-color: rgba(46, 204, 113, 0.2);",
    "working": "color: #f1c40f; background-color: rgba(241, 196, 15, 0.2);",
    "success": "color: #2ecc71; background-color: rgba(46, 204, 113, 0.2);",
    "error": "color: #e67e22; background-color: rgba(230, 126, 34, 0.2);"
}

# Dynamic status colors based on current theme
def get_status_colors():
    """Get status colors for current theme"""
    return STATUS_COLORS_DARK if theme_manager.current_theme == "dark" else STATUS_COLORS_LIGHT

# For backward compatibility
STATUS_COLORS = STATUS_COLORS_LIGHT

# Light theme stylesheet
APP_STYLE_LIGHT = """
            QWidget {
                background-color: #f5f5f5;
                font-family: Arial, sans-serif;
                color: #2c3e50;
            }
            
            QLabel#title {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                margin: 10px 0;
                padding: 10px;
            }
            
            QLabel#subtitle {
                font-size: 14px;
                color: #7f8c8d;
                margin-bottom: 20px;
            }
            
            QFrame#separator {
                color: #bdc3c7;
                margin: 10px 0;
            }
            
            QGroupBox#group {
                font-size: 16px;
                font-weight: bold;
                color: #34495e;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                margin: 10px 0;
                padding-top: 15px;
            }
            
            QGroupBox#group::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                background-color: #f5f5f5;
            }
            
            QLabel#label {
                font-size: 14px;
                font-weight: 600;
                color: #2c3e50;
                margin: 5px 0;
            }
            
            QLabel#info_label {
                font-size: 12px;
                color: #7f8c8d;
                font-style: italic;
                margin: 5px 0;
            }
            
            QLineEdit#input {
                padding: 12px 15px;
                font-size: 14px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                background-color: white;
                color: #2c3e50;
                selection-background-color: #3498db;
            }
            
            QLineEdit#input:focus {
                border-color: #3498db;
                outline: none;
            }
            
            QComboBox {
                padding: 8px 12px;
                font-size: 14px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                background-color: white;
                color: #2c3e50;
                min-width: 200px;
            }
            
            QComboBox:focus {
                border-color: #3498db;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #7f8c8d;
                margin-right: 10px;
            }
            
            QComboBox QAbstractItemView {
                background-color: white;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                selection-background-color: #3498db;
                selection-color: white;
            }
            
            QPushButton {
                font-size: 14px;
                font-weight: 600;
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                min-height: 20px;
            }
            
            QPushButton#primary_btn {
                background-color: #3498db;
                color: white;
            }
            
            QPushButton#primary_btn:hover {
                background-color: #2980b9;
            }
            
            QPushButton#primary_btn:pressed {
                background-color: #21618c;
            }
            
            QPushButton#secondary_btn {
                background-color: #95a5a6;
                color: white;
            }
            
            QPushButton#secondary_btn:hover {
                background-color: #7f8c8d;
            }
            
            QPushButton#secondary_btn:pressed {
                background-color: #6c7b7d;
            }
            
            QPushButton#success_btn {
                background-color: #27ae60;
                color: white;
            }
            
            QPushButton#success_btn:hover {
                background-color: #229954;
            }
            
            QPushButton#success_btn:pressed {
                background-color: #1e8449;
            }
            
            QPushButton#accent_btn {
                background-color: #e74c3c;
                color: white;
            }
            
            QPushButton#accent_btn:hover {
                background-color: #c0392b;
            }
            
            QPushButton#accent_btn:pressed {
                background-color: #a93226;
            }
            
            QPushButton#theme_btn {
                background-color: #9b59b6;
                color: white;
            }
            
            QPushButton#theme_btn:hover {
                background-color: #8e44ad;
            }
            
            QPushButton#theme_btn:pressed {
                background-color: #7d3c98;
            }
            
            QTextEdit#log {
                background-color: #2c3e50;
                color: #ecf0f1;
                border: 2px solid #34495e;
                border-radius: 8px;
                font-family: 'Monaco', 'Courier New', monospace;
                font-size: 12px;
                padding: 10px;
                line-height: 1.4;
            }
            
            QScrollBar:vertical {
                background-color: #34495e;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #7f8c8d;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #95a5a6;
            }
            
            QLabel#status_label {
                font-size: 14px;
                font-weight: bold;
                color: #27ae60;
                padding: 5px 10px;
                border-radius: 5px;
                background-color: rgba(39, 174, 96, 0.1);
            }
            
            QLabel#elapsed_label {
                font-size: 12px;
                color: #7f8c8d;
                font-family: 'Monaco', 'Courier New', monospace;
            }
            
            QProgressBar#progress_bar {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
                background-color: #ecf0f1;
                height: 25px;
            }
            
            QProgressBar#progress_bar::chunk {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #3498db, stop: 1 #2980b9);
                border-radius: 6px;
                margin: 2px;
            }
            
            /* Dialog styles */
            QDialog {
                background-color: #f5f5f5;
                color: #2c3e50;
            }
            
            QInputDialog {
                background-color: #f5f5f5;
                color: #2c3e50;
            }
            
            QInputDialog QLineEdit {
                background-color: white;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                padding: 8px;
            }
            
            QInputDialog QComboBox {
                background-color: white;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                padding: 8px;
            }
            
            QInputDialog QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            
            QInputDialog QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #7f8c8d;
            }
            
            QInputDialog QComboBox QAbstractItemView {
                background-color: white;
                color: #2c3e50;
                border: 1px solid #bdc3c7;
                selection-background-color: #3498db;
                selection-color: white;
            }
            
            /* Dialog Button Styles */
            QDialog QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 600;
                min-width: 80px;
            }
            
            QDialog QPushButton:hover {
                background-color: #2980b9;
            }
            
            QDialog QPushButton:pressed {
                background-color: #21618c;
            }
            
            QInputDialog QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 600;
                min-width: 80px;
            }
            
            QInputDialog QPushButton:hover {
                background-color: #2980b9;
            }
            
            QInputDialog QPushButton:pressed {
                background-color: #21618c;
            }
            
            QMessageBox {
                background-color: #f5f5f5;
                color: #2c3e50;
            }
            
            QMessageBox QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 600;
                min-width: 80px;
            }
            
            QMessageBox QPushButton:hover {
                background-color: #2980b9;
            }
            
            QMessageBox QPushButton:pressed {
                background-color: #21618c;
            }
        """

# Dark theme stylesheet
APP_STYLE_DARK = """
            QWidget {
                background-color: #2b2b2b;
                font-family: Arial, sans-serif;
                color: #ffffff;
            }
            
            QLabel#title {
                font-size: 28px;
                font-weight: bold;
                color: #ffffff;
                margin: 10px 0;
                padding: 10px;
            }
            
            QLabel#subtitle {
                font-size: 14px;
                color: #bdc3c7;
                margin-bottom: 20px;
            }
            
            QFrame#separator {
                color: #555555;
                margin: 10px 0;
            }
            
            QGroupBox#group {
                font-size: 16px;
                font-weight: bold;
                color: #ffffff;
                border: 2px solid #555555;
                border-radius: 10px;
                margin: 10px 0;
                padding-top: 15px;
            }
            
            QGroupBox#group::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                background-color: #2b2b2b;
            }
            
            QLabel#label {
                font-size: 14px;
                font-weight: 600;
                color: #ffffff;
                margin: 5px 0;
            }
            
            QLabel#info_label {
                font-size: 12px;
                color: #bdc3c7;
                font-style: italic;
                margin: 5px 0;
            }
            
            QLineEdit#input {
                padding: 12px 15px;
                font-size: 14px;
                border: 2px solid #555555;
                border-radius: 8px;
                background-color: #3c3c3c;
                color: #ffffff;
                selection-background-color: #5dade2;
            }
            
            QLineEdit#input:focus {
                border-color: #5dade2;
                outline: none;
            }
            
            QComboBox {
                padding: 8px 12px;
                font-size: 14px;
                border: 2px solid #555555;
                border-radius: 8px;
                background-color: #3c3c3c;
                color: #ffffff;
                min-width: 200px;
            }
            
            QComboBox:focus {
                border-color: #5dade2;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #bdc3c7;
                margin-right: 10px;
            }
            
            QComboBox QAbstractItemView {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 2px solid #555555;
                border-radius: 8px;
                selection-background-color: #5dade2;
                selection-color: white;
            }
            
            QPushButton {
                font-size: 14px;
                font-weight: 600;
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                min-height: 20px;
            }
            
            QPushButton#primary_btn {
                background-color: #5dade2;
                color: white;
            }
            
            QPushButton#primary_btn:hover {
                background-color: #3498db;
            }
            
            QPushButton#primary_btn:pressed {
                background-color: #2980b9;
            }
            
            QPushButton#secondary_btn {
                background-color: #7f8c8d;
                color: white;
            }
            
            QPushButton#secondary_btn:hover {
                background-color: #95a5a6;
            }
            
            QPushButton#secondary_btn:pressed {
                background-color: #6c7b7d;
            }
            
            QPushButton#success_btn {
                background-color: #2ecc71;
                color: white;
            }
            
            QPushButton#success_btn:hover {
                background-color: #27ae60;
            }
            
            QPushButton#success_btn:pressed {
                background-color: #229954;
            }
            
            QPushButton#accent_btn {
                background-color: #e67e22;
                color: white;
            }
            
            QPushButton#accent_btn:hover {
                background-color: #d35400;
            }
            
            QPushButton#accent_btn:pressed {
                background-color: #a04000;
            }
            
            QPushButton#theme_btn {
                background-color: #af7ac5;
                color: white;
            }
            
            QPushButton#theme_btn:hover {
                background-color: #9b59b6;
            }
            
            QPushButton#theme_btn:pressed {
                background-color: #8e44ad;
            }
            
            QTextEdit#log {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 2px solid #555555;
                border-radius: 8px;
                font-family: 'Monaco', 'Courier New', monospace;
                font-size: 12px;
                padding: 10px;
                line-height: 1.4;
            }
            
            QScrollBar:vertical {
                background-color: #3c3c3c;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #7f8c8d;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #95a5a6;
            }
            
            QLabel#status_label {
                font-size: 14px;
                font-weight: bold;
                color: #2ecc71;
                padding: 5px 10px;
                border-radius: 5px;
                background-color: rgba(46, 204, 113, 0.2);
            }
            
            QLabel#elapsed_label {
                font-size: 12px;
                color: #bdc3c7;
                font-family: 'Monaco', 'Courier New', monospace;
            }
            
            QProgressBar#progress_bar {
                border: 2px solid #555555;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
                background-color: #3c3c3c;
                height: 25px;
                color: #ffffff;
            }
            
            QProgressBar#progress_bar::chunk {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #5dade2, stop: 1 #3498db);
                border-radius: 6px;
                margin: 2px;
            }
            
            /* Dialog styles */
            QDialog {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            
            QInputDialog {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            
            QInputDialog QLineEdit {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 2px solid #555555;
                border-radius: 4px;
                padding: 8px;
            }
            
            QInputDialog QComboBox {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 2px solid #555555;
                border-radius: 4px;
                padding: 8px;
            }
            
            QInputDialog QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            
            QInputDialog QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #bdc3c7;
            }
            
            QInputDialog QComboBox QAbstractItemView {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555555;
                selection-background-color: #5dade2;
                selection-color: white;
            }
            
            /* Dialog Button Styles */
            QDialog QPushButton {
                background-color: #5dade2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 600;
                min-width: 80px;
            }
            
            QDialog QPushButton:hover {
                background-color: #3498db;
            }
            
            QDialog QPushButton:pressed {
                background-color: #2980b9;
            }
            
            QInputDialog QPushButton {
                background-color: #5dade2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 600;
                min-width: 80px;
            }
            
            QInputDialog QPushButton:hover {
                background-color: #3498db;
            }
            
            QInputDialog QPushButton:pressed {
                background-color: #2980b9;
            }
            
            QMessageBox {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            
            QMessageBox QPushButton {
                background-color: #5dade2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 600;
                min-width: 80px;
            }
            
            QMessageBox QPushButton:hover {
                background-color: #3498db;
            }
            
            QMessageBox QPushButton:pressed {
                background-color: #2980b9;
            }
        """

# Dynamic theme functions
def get_app_style():
    """Get the current theme's app style"""
    return APP_STYLE_DARK if theme_manager.current_theme == "dark" else APP_STYLE_LIGHT

def toggle_theme():
    """Toggle between light and dark themes"""
    return theme_manager.toggle_theme()

def set_theme(theme):
    """Set specific theme"""
    return theme_manager.set_theme(theme)

def get_current_theme():
    """Get current theme name"""
    return theme_manager.get_current_theme()

# For backward compatibility
APP_STYLE = APP_STYLE_LIGHT
