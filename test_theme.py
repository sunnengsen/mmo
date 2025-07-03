#!/usr/bin/env python3
"""
Test script to validate theme switching functionality
"""

from ui_styles_new import (
    theme_manager, get_app_style, toggle_theme, 
    get_current_theme, get_status_colors
)

def test_theme_switching():
    """Test the theme switching functionality"""
    print("🎨 Testing Theme Switching Functionality")
    print("=" * 50)
    
    # Test initial state
    print(f"Initial theme: {get_current_theme()}")
    print(f"Theme manager state: {theme_manager.current_theme}")
    
    # Test theme toggle
    print("\n🔄 Testing theme toggle...")
    new_theme = toggle_theme()
    print(f"After toggle: {new_theme}")
    print(f"get_current_theme(): {get_current_theme()}")
    
    # Test toggle again
    print("\n🔄 Testing theme toggle again...")
    new_theme = toggle_theme()
    print(f"After second toggle: {new_theme}")
    print(f"get_current_theme(): {get_current_theme()}")
    
    # Test status colors
    print("\n🎨 Testing status colors...")
    status_colors = get_status_colors()
    print(f"Current status colors: {list(status_colors.keys())}")
    
    # Test style retrieval
    print("\n🖌️ Testing style retrieval...")
    style = get_app_style()
    print(f"Style length: {len(style)} characters")
    print(f"Contains 'QWidget': {'QWidget' in style}")
    
    # Test both themes
    print("\n🌓 Testing both themes...")
    for theme in ["light", "dark"]:
        theme_manager.set_theme(theme)
        style = get_app_style()
        colors = get_status_colors()
        print(f"{theme.title()} theme:")
        print(f"  - Style length: {len(style)} characters")
        print(f"  - Status colors: {list(colors.keys())}")
        print(f"  - Ready color: {colors['ready'][:50]}...")
    
    print("\n✅ Theme switching test completed successfully!")

if __name__ == "__main__":
    test_theme_switching()
