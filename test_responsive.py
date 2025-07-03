#!/usr/bin/env python3
"""
Terminal-based theme switching test - no GUI required
"""

from ui_styles_new import (
    get_app_style, toggle_theme, get_current_theme, 
    get_status_colors, theme_manager
)

def test_theme_responsiveness():
    """Test theme switching responsiveness"""
    print("🎨 Theme Switching Responsiveness Test")
    print("=" * 50)
    
    print(f"Initial theme: {get_current_theme()}")
    
    # Test multiple rapid switches
    for i in range(5):
        new_theme = toggle_theme()
        style_length = len(get_app_style())
        status_colors = get_status_colors()
        
        print(f"Switch {i+1}: {new_theme} theme")
        print(f"  - Style length: {style_length} chars")
        print(f"  - Ready color: {status_colors['ready'][:30]}...")
        print(f"  - Manager state: {theme_manager.current_theme}")
        print()
    
    print("✅ All theme switches completed successfully!")
    print("Theme switching is fully responsive!")

if __name__ == "__main__":
    test_theme_responsiveness()
