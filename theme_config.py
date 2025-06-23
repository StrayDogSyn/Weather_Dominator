"""
Glassmorphic Style Configuration for Weather Dominator
Contains color schemes, fonts, and styling constants
"""

class GlassmorphicTheme:
    """Configuration class for glassmorphic styling"""
    
    # Background colors
    WINDOW_BG = '#000000'
    CONTAINER_BG = '#1a1a2e'
    GLASS_BG = '#16213e'
    CONTENT_BG = '#16213e'
    
    # Accent colors
    PRIMARY_ACCENT = '#4a9eff'
    SECONDARY_ACCENT = '#7bb3ff'
    HIGHLIGHT = '#4a6fa5'
    BORDER = '#0f3460'
    
    # Gradient colors for glassmorphic effect
    GRADIENT_COLORS = [
        '#1e2a5a',
        '#1a2451', 
        '#161e48',
        '#12183f'
    ]
    
    # Text colors
    TITLE_COLOR = '#4a9eff'
    SUBTITLE_COLOR = '#7bb3ff'
    TEXT_COLOR = '#ffffff'
    MUTED_TEXT = '#b0b0b0'
    
    # Button colors
    BUTTON_BG = '#2d4059'
    BUTTON_FG = '#ffffff'
    BUTTON_ACTIVE_BG = '#4a6fa5'
    BUTTON_HOVER_BG = '#3a5068'
    
    # Danger/Close button
    DANGER_COLOR = '#ff6b6b'
    
    # Fonts
    TITLE_FONT = ('Arial', 24, 'bold')
    SUBTITLE_FONT = ('Arial', 12)
    BODY_FONT = ('Arial', 10)
    BUTTON_FONT = ('Arial', 10, 'bold')
    SECTION_FONT = ('Arial', 12, 'bold')
    LABEL_FONT = ('Arial', 9, 'bold')
    SMALL_FONT = ('Arial', 8)
    LARGE_FONT = ('Arial', 18, 'bold')
    
    # Input colors
    INPUT_BG = '#1a2451'
    INPUT_FG = '#ffffff'
    INPUT_BORDER = '#4a6fa5'
    
    # Window properties
    WINDOW_ALPHA = 0.95
    BORDER_WIDTH = 1
    PADDING_LARGE = 20
    PADDING_MEDIUM = 10
    PADDING_SMALL = 5
    
    # Glass effect properties
    GLASS_HIGHLIGHT_HEIGHT = 2
    GRADIENT_FRAME_HEIGHT = 1
    SEPARATOR_HEIGHT = 1

# COBRA themed color scheme (alternative)
class CobraTheme(GlassmorphicTheme):
    """COBRA-specific color theme"""
    
    # COBRA signature colors
    PRIMARY_ACCENT = '#dc143c'  # Crimson red
    SECONDARY_ACCENT = '#ff6b6b'  # Light red
    HIGHLIGHT = '#8b0000'  # Dark red
    
    # Updated text colors for COBRA theme
    TITLE_COLOR = '#dc143c'
    SUBTITLE_COLOR = '#ff6b6b'
