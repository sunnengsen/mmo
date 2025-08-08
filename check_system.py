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
    
    # First try global command
    try:
        result = subprocess.run([command, '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"   ✅ {display_name} (OK) - {version_line}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
        pass
    
    # Try in virtual environment if global fails
    import os
    venv_path = os.path.join(os.getcwd(), '.venv', 'bin', command)
    if os.path.exists(venv_path):
        try:
            result = subprocess.run([venv_path, '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                print(f"   ✅ {display_name} (OK - in venv) - {version_line}")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            pass
    
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
        print("   .venv/bin/python app.py")
        print("   or")
        print("   .venv/bin/python video_tool_app.py")
        print("   or")
        print("   .venv/bin/python video_tool_app_themed.py  (with theme switching)")
        print("   or")
        print("   .venv/bin/python simple_theme_demo.py  (theme demo)")
        print()
        print("💡 Alternatively, activate the virtual environment first:")
        print("   source .venv/bin/activate")
        print("   python app.py")
        return True
    else:
        print("⚠️  Some checks failed. Please address the missing requirements.")
        print()
        print("💡 Quick fixes:")
        if not check_module('PyQt6', silent=True):
            print("   .venv/bin/pip install PyQt6")
        if not check_command('ffmpeg', silent=True):
            print("   Install FFmpeg from https://ffmpeg.org/download.html")
            print("   On macOS: brew install ffmpeg")
        if not check_command('yt-dlp', silent=True):
            print("   .venv/bin/pip install yt-dlp")
        print()
        print("📖 For detailed setup instructions, see SETUP_GUIDE.md")
        return False


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
        # Try global command first
        version_flags = ['--version', '-version', '-V']  # Different version flags
        for flag in version_flags:
            try:
                result = subprocess.run([command, flag], 
                                      capture_output=True, 
                                      timeout=5)
                if result.returncode == 0:
                    return True
            except:
                continue
        
        # Try common system paths
        import os
        common_paths = ['/usr/local/bin', '/opt/homebrew/bin', '/usr/bin']
        for path in common_paths:
            full_path = os.path.join(path, command)
            if os.path.exists(full_path):
                for flag in version_flags:
                    try:
                        result = subprocess.run([full_path, flag], 
                                              capture_output=True, 
                                              timeout=5)
                        if result.returncode == 0:
                            return True
                    except:
                        continue
        
        # Try in virtual environment
        venv_path = os.path.join(os.getcwd(), '.venv', 'bin', command)
        if os.path.exists(venv_path):
            for flag in version_flags:
                try:
                    result = subprocess.run([venv_path, flag], 
                                          capture_output=True, 
                                          timeout=5)
                    if result.returncode == 0:
                        return True
                except:
                    continue
        return False
    else:
        # Original implementation with venv support
        if display_name is None:
            display_name = command
        
        print(f"🔧 Checking {display_name}...")
        
        version_flags = ['--version', '-version', '-V']  # Different version flags
        
        # First try global command
        for flag in version_flags:
            try:
                result = subprocess.run([command, flag], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=10)
                if result.returncode == 0:
                    version_line = result.stdout.split('\n')[0]
                    print(f"   ✅ {display_name} (OK) - {version_line}")
                    return True
            except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
                continue
        
        # Try common system paths
        import os
        common_paths = ['/usr/local/bin', '/opt/homebrew/bin', '/usr/bin']
        for path in common_paths:
            full_path = os.path.join(path, command)
            if os.path.exists(full_path):
                for flag in version_flags:
                    try:
                        result = subprocess.run([full_path, flag], 
                                              capture_output=True, 
                                              text=True, 
                                              timeout=10)
                        if result.returncode == 0:
                            version_line = result.stdout.split('\n')[0]
                            print(f"   ✅ {display_name} (OK) - {version_line}")
                            return True
                    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
                        continue
        
        # Try in virtual environment if global fails
        venv_path = os.path.join(os.getcwd(), '.venv', 'bin', command)
        if os.path.exists(venv_path):
            for flag in version_flags:
                try:
                    result = subprocess.run([venv_path, flag], 
                                          capture_output=True, 
                                          text=True, 
                                          timeout=10)
                    if result.returncode == 0:
                        version_line = result.stdout.split('\n')[0]
                        print(f"   ✅ {display_name} (OK - in venv) - {version_line}")
                        return True
                except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
                    continue
        
        print(f"   ❌ {display_name} (Not found)")
        return False

if __name__ == "__main__":
    main()
