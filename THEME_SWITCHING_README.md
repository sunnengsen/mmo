# Theme Switching Feature for Video Tool Pro

This update adds dark mode and light mode switching capabilities to your Video Tool Pro application.

## 🌟 New Features

- **Light Mode**: Clean, bright interface (default)
- **Dark Mode**: Easy-on-the-eyes dark theme
- **Theme Toggle**: Switch between themes with a single button click
- **Persistent Styling**: All UI elements automatically update when theme changes

## 📁 Files Added/Modified

### New Files:
- `ui_styles_new.py` - Enhanced UI styles with theme switching support
- `theme_demo.py` - Demo application showing theme switching
- `integration_guide.py` - Step-by-step integration guide
- `test_theme.py` - Test script to validate theme functionality

### Key Components:

#### 1. `ui_styles_new.py`
- **ThemeManager Class**: Manages theme state and switching
- **Light Theme**: `APP_STYLE_LIGHT` with bright colors
- **Dark Theme**: `APP_STYLE_DARK` with dark colors
- **Dynamic Functions**: `get_app_style()`, `toggle_theme()`, `get_status_colors()`

#### 2. Theme Functions
```python
from ui_styles_new import get_app_style, toggle_theme, get_current_theme

# Get current theme style
style = get_app_style()

# Toggle between light and dark
new_theme = toggle_theme()

# Get current theme name
current = get_current_theme()  # returns "light" or "dark"
```

## 🚀 How to Integrate

### Option 1: Use the Demo App
```bash
python theme_demo.py
```

### Option 2: Integrate into Existing App

1. **Update imports** in your `video_tool_app.py`:
```python
# Replace this:
from ui_styles import APP_STYLE, STATUS_COLORS

# With this:
from ui_styles_new import (
    get_app_style, toggle_theme, get_current_theme, 
    get_status_colors
)
```

2. **Add theme button** to your UI:
```python
def _create_header(self, main_layout):
    header_layout = QHBoxLayout()
    
    # Your existing title
    title = QLabel("🎬 Video Tool Pro")
    title.setObjectName("title")
    header_layout.addWidget(title)
    
    # Theme toggle button
    self.theme_btn = QPushButton("🌙 Dark Mode")
    self.theme_btn.setObjectName("theme_btn")
    self.theme_btn.clicked.connect(self.toggle_theme)
    header_layout.addWidget(self.theme_btn)
    
    main_layout.addLayout(header_layout)
```

3. **Update styling method**:
```python
def setup_styling(self):
    """Apply CSS styling with theme support"""
    self.setStyleSheet(get_app_style())
```

4. **Add theme toggle method**:
```python
def toggle_theme(self):
    """Toggle between light and dark themes"""
    new_theme = toggle_theme()
    self.setStyleSheet(get_app_style())
    
    # Update button text
    if new_theme == "dark":
        self.theme_btn.setText("☀️ Light Mode")
    else:
        self.theme_btn.setText("🌙 Dark Mode")
    
    # Update status colors
    status_colors = get_status_colors()
    self.status_label.setStyleSheet(status_colors["ready"])
```

## 🎨 Theme Differences

### Light Mode
- Background: Light gray (#f5f5f5)
- Text: Dark blue (#2c3e50)
- Buttons: Blue theme
- Inputs: White backgrounds

### Dark Mode
- Background: Dark gray (#2b2b2b)
- Text: White (#ffffff)
- Buttons: Lighter blue theme
- Inputs: Dark gray backgrounds

## 🧪 Testing

Run the test script to verify functionality:
```bash
python test_theme.py
```

## 📋 Status Colors

Both themes include status colors for:
- **Ready**: Green
- **Working**: Orange
- **Success**: Green
- **Error**: Red

Colors automatically adjust based on current theme.

## 🔧 Advanced Usage

### Manual Theme Setting
```python
from ui_styles_new import theme_manager

# Set specific theme
theme_manager.set_theme("dark")  # or "light"

# Get current theme
current_theme = theme_manager.get_current_theme()
```

### Custom Status Colors
```python
from ui_styles_new import get_status_colors

status_colors = get_status_colors()
self.my_label.setStyleSheet(status_colors["success"])
```

## 🔄 Migration from Old Styles

1. Replace imports
2. Change `APP_STYLE` to `get_app_style()`
3. Change `STATUS_COLORS` to `get_status_colors()`
4. Add theme toggle button
5. Add theme toggle method

## 🎯 Benefits

- **Better UX**: Users can choose their preferred theme
- **Eye Comfort**: Dark mode reduces eye strain
- **Modern Look**: Professional appearance with theme switching
- **Easy Integration**: Drop-in replacement for existing styles
- **Backward Compatible**: Old code still works with minimal changes

## 📝 Notes

- Default theme is light mode
- Theme preference is not persistent across app restarts (can be extended)
- All UI elements update automatically when theme changes
- Button styles include hover and pressed states for both themes
