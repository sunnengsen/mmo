"""
UI Styling constants and styles for the Video Tool Pro application.
"""

# Status color constants
STATUS_COLORS = {
    "ready": "color: #27ae60; background-color: rgba(39, 174, 96, 0.1);",
    "working": "color: #f39c12; background-color: rgba(243, 156, 18, 0.1);",
    "success": "color: #27ae60; background-color: rgba(39, 174, 96, 0.1);",
    "error": "color: #e74c3c; background-color: rgba(231, 76, 60, 0.1);"
}

# Main application stylesheet
APP_STYLE = """
            QWidget {
                background-color: #f5f5f5;
                font-family: Arial, sans-serif;
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
            
            QMessageBox {
                background-color: #f5f5f5;
                color: #2c3e50;
            }
        """
