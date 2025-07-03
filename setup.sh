#!/bin/bash
# 🚀 Video Tool Pro - macOS/Linux Setup Script

echo "🎬 Video Tool Pro - Automated Setup Script"
echo "==========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3 is installed
check_python() {
    print_status "Checking Python installation..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        print_success "Python 3 found: $PYTHON_VERSION"
        return 0
    else
        print_error "Python 3 is not installed!"
        print_status "Please install Python 3.8+ from https://www.python.org/downloads/"
        return 1
    fi
}

# Check if pip is installed
check_pip() {
    print_status "Checking pip installation..."
    if command -v pip3 &> /dev/null; then
        print_success "pip3 found"
        return 0
    else
        print_error "pip3 is not installed!"
        return 1
    fi
}

# Check if FFmpeg is installed
check_ffmpeg() {
    print_status "Checking FFmpeg installation..."
    if command -v ffmpeg &> /dev/null; then
        print_success "FFmpeg found"
        return 0
    else
        print_warning "FFmpeg is not installed!"
        print_status "Installing FFmpeg..."
        
        # Detect OS and install FFmpeg
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            if command -v brew &> /dev/null; then
                brew install ffmpeg
                print_success "FFmpeg installed via Homebrew"
            else
                print_error "Homebrew not found. Please install FFmpeg manually:"
                print_status "Visit: https://ffmpeg.org/download.html"
                return 1
            fi
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            if command -v apt &> /dev/null; then
                sudo apt update
                sudo apt install -y ffmpeg
                print_success "FFmpeg installed via apt"
            elif command -v yum &> /dev/null; then
                sudo yum install -y ffmpeg
                print_success "FFmpeg installed via yum"
            else
                print_error "Package manager not found. Please install FFmpeg manually."
                return 1
            fi
        else
            print_error "Unsupported OS. Please install FFmpeg manually."
            return 1
        fi
    fi
}

# Create virtual environment
create_venv() {
    print_status "Creating virtual environment..."
    if [ -d "venv" ]; then
        print_warning "Virtual environment already exists"
    else
        python3 -m venv venv
        print_success "Virtual environment created"
    fi
}

# Activate virtual environment and install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_success "Requirements installed"
    else
        print_error "requirements.txt not found!"
        return 1
    fi
    
    # Install yt-dlp
    pip install yt-dlp
    print_success "yt-dlp installed"
}

# Test the installation
test_installation() {
    print_status "Testing installation..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Test Python modules
    python3 -c "import PyQt6; print('PyQt6: OK')" 2>/dev/null
    if [ $? -eq 0 ]; then
        print_success "PyQt6 test passed"
    else
        print_error "PyQt6 test failed"
        return 1
    fi
    
    # Test theme module
    python3 -c "import ui_styles_new; print('UI Styles: OK')" 2>/dev/null
    if [ $? -eq 0 ]; then
        print_success "UI Styles test passed"
    else
        print_error "UI Styles test failed"
        return 1
    fi
    
    # Test FFmpeg
    ffmpeg -version > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        print_success "FFmpeg test passed"
    else
        print_error "FFmpeg test failed"
        return 1
    fi
    
    # Test yt-dlp
    yt-dlp --version > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        print_success "yt-dlp test passed"
    else
        print_error "yt-dlp test failed"
        return 1
    fi
}

# Main setup function
main() {
    print_status "Starting Video Tool Pro setup..."
    
    # Check prerequisites
    if ! check_python; then
        exit 1
    fi
    
    if ! check_pip; then
        exit 1
    fi
    
    if ! check_ffmpeg; then
        exit 1
    fi
    
    # Setup project
    create_venv
    install_dependencies
    
    # Test installation
    if test_installation; then
        echo ""
        print_success "🎉 Setup completed successfully!"
        echo ""
        print_status "To run the application:"
        echo "  1. Activate virtual environment: source venv/bin/activate"
        echo "  2. Run the app: python video_tool_app.py"
        echo "  3. Or run with themes: python video_tool_app_themed.py"
        echo "  4. Or test themes: python simple_theme_demo.py"
        echo ""
        print_status "Next steps:"
        echo "  - Read README.md for detailed information"
        echo "  - Check THEME_SWITCHING_README.md for theme features"
        echo "  - Run 'python test_theme.py' to test theme switching"
        echo ""
    else
        print_error "Setup failed! Please check the errors above."
        exit 1
    fi
}

# Run main function
main
