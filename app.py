import sys
from PyQt6.QtWidgets import QApplication
from video_tool_app import VideoToolApp


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show window
    window = VideoToolApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
