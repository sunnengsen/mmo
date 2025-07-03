#!/usr/bin/env python3
"""
System Requirements Check for Video Tool Pro
Run this script to verify that your system is ready to run the application.
"""

import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Need Python 3.8+)")
        return False

def check_module(module_name, display_name=None):
    """Check if a Python module is available"""
    if display_name is None:
        display_name = module_name
    
    print(f"📦 Checking {display_name}...")
    try:
        importlib.import_module(module_name)
        print(f"   ✅ {display_name} (OK)")
        return True
    except ImportError:
        print(f"   ❌ {display_name} (Missing)")
        return False

def check_command(command, display_name=None):
    """Check if a system command is available"""
    if display_name is None:
        display_name = command
    
    print(f"🔧 Checking {display_name}...")
    try:
        result = subprocess.run([command, '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"   ✅ {display_name} (OK) - {version_line}")
            return True
        else:
            print(f"   ❌ {display_name} (Not working)")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
        print(f"   ❌ {display_name} (Not found)")
        return False

def check_project_files():
    """Check if required project files exist"""
    print("📁 Checking project files...")
    import os
    
    required_files = [
        'requirements.txt',
        'ui_styles_new.py',
        'video_tool_app.py',
        'video_operations.py'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (Missing)")
            missing_files.append(file)
    
    return len(missing_files) == 0

def main():
    """Run all system checks"""
    print("🎬 Video Tool Pro - System Requirements Check")
    print("=" * 50)
    
    checks_passed = 0
    total_checks = 0
    
    # Check Python version
    total_checks += 1
    if check_python_version():
        checks_passed += 1
    
    print()
    
    # Check Python modules
    modules_to_check = [
        ('PyQt6', 'PyQt6 GUI Framework'),
        ('ui_styles_new', 'Theme System'),
        ('video_operations', 'Video Operations'),
    ]
    
    for module, display_name in modules_to_check:
        total_checks += 1
        if check_module(module, display_name):
            checks_passed += 1
    
    print()
    
    # Check system commands
    commands_to_check = [
        ('ffmpeg', 'FFmpeg Video Processor'),
        ('yt-dlp', 'Video Downloader'),
    ]
    
    for command, display_name in commands_to_check:
        total_checks += 1
        if check_command(command, display_name):
            checks_passed += 1
    
    print()
    
    # Check project files
    total_checks += 1
    if check_project_files():
        checks_passed += 1
    
    print()
    print("=" * 50)
    print(f"📊 Summary: {checks_passed}/{total_checks} checks passed")
    
    if checks_passed == total_checks:
        print("🎉 All checks passed! Your system is ready to run Video Tool Pro.")
        print()
        print("🚀 To start the application:")
        print("   python video_tool_app.py")
        print("   or")
        print("   python video_tool_app_themed.py  (with theme switching)")
        print("   or")
        print("   python simple_theme_demo.py  (theme demo)")
        return True
    else:
        print("⚠️  Some checks failed. Please address the missing requirements.")
        print()
        print("💡 Quick fixes:")
        if not check_module('PyQt6', silent=True):
            print("   pip install PyQt6")
        if not check_command('ffmpeg', silent=True):
            print("   Install FFmpeg from https://ffmpeg.org/download.html")
        if not check_command('yt-dlp', silent=True):
            print("   pip install yt-dlp")
        print()
        print("📖 For detailed setup instructions, see SETUP_GUIDE.md")
        return False

def check_module_silent(module_name):
    """Silently check if a module is available"""
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

def check_command_silent(command):
    """Silently check if a command is available"""
    try:
        result = subprocess.run([command, '--version'], 
                              capture_output=True, 
                              timeout=5)
        return result.returncode == 0
    except:
        return False

# Add silent check functions for the summary
def check_module(module_name, display_name=None, silent=False):
    if silent:
        try:
            importlib.import_module(module_name)
            return True
        except ImportError:
            return False
    else:
        # Original implementation
        if display_name is None:
            display_name = module_name
        
        print(f"📦 Checking {display_name}...")
        try:
            importlib.import_module(module_name)
            print(f"   ✅ {display_name} (OK)")
            return True
        except ImportError:
            print(f"   ❌ {display_name} (Missing)")
            return False

def check_command(command, display_name=None, silent=False):
    if silent:
        try:
            result = subprocess.run([command, '--version'], 
                                  capture_output=True, 
                                  timeout=5)
            return result.returncode == 0
        except:
            return False
    else:
        # Original implementation
        if display_name is None:
            display_name = command
        
        print(f"🔧 Checking {display_name}...")
        try:
            result = subprocess.run([command, '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                print(f"   ✅ {display_name} (OK) - {version_line}")
                return True
            else:
                print(f"   ❌ {display_name} (Not working)")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            print(f"   ❌ {display_name} (Not found)")
            return False

if __name__ == "__main__":
    main()
