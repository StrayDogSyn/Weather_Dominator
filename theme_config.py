"""
Glassmorphic Style Configuration for Weather Dominator
Contains color schemes, fonts, and styling constants
"""

from src.constants import ThemeColors, FontConfig


class GlassmorphicTheme:
    """Configuration class for glassmorphic styling"""

    # Background colors - using centralized constants
    WINDOW_BG = ThemeColors.WINDOW_BG
    CONTAINER_BG = ThemeColors.CONTAINER_BG
    GLASS_BG = ThemeColors.GLASS_BG
    CONTENT_BG = ThemeColors.CONTENT_BG

    # Accent colors
    PRIMARY_ACCENT = ThemeColors.PRIMARY_ACCENT
    SECONDARY_ACCENT = ThemeColors.SECONDARY_ACCENT
    HIGHLIGHT = ThemeColors.HIGHLIGHT
    BORDER = ThemeColors.BORDER

    # Gradient colors for glassmorphic effect
    GRADIENT_COLORS = ThemeColors.GRADIENT_COLORS

    # Text colors
    TITLE_COLOR = ThemeColors.TITLE_COLOR
    SUBTITLE_COLOR = ThemeColors.SUBTITLE_COLOR
    TEXT_COLOR = ThemeColors.TEXT_COLOR
    MUTED_TEXT = ThemeColors.MUTED_TEXT

    # Button colors
    BUTTON_BG = ThemeColors.BUTTON_BG
    BUTTON_FG = ThemeColors.BUTTON_FG
    BUTTON_ACTIVE_BG = ThemeColors.BUTTON_ACTIVE_BG
    BUTTON_HOVER_BG = ThemeColors.BUTTON_HOVER_BG

    # Danger/Close button
    DANGER_COLOR = ThemeColors.DANGER_COLOR

    # Fonts - using centralized font configuration
    TITLE_FONT = FontConfig.TITLE_FONT
    SUBTITLE_FONT = FontConfig.SUBTITLE_FONT
    BODY_FONT = FontConfig.BODY_FONT
    BUTTON_FONT = FontConfig.BUTTON_FONT
    SECTION_FONT = FontConfig.SECTION_FONT
    LABEL_FONT = FontConfig.LABEL_FONT
    SMALL_FONT = FontConfig.SMALL_FONT
    LARGE_FONT = FontConfig.LARGE_FONT

    # Input colors
    INPUT_BG = ThemeColors.INPUT_BG
    INPUT_FG = ThemeColors.INPUT_FG
    INPUT_BORDER = ThemeColors.INPUT_BORDER

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
    PRIMARY_ACCENT = "#dc143c"  # Crimson red
    SECONDARY_ACCENT = "#ff6b6b"  # Light red
    HIGHLIGHT = "#8b0000"  # Dark red

    # Updated text colors for COBRA theme
    TITLE_COLOR = "#dc143c"
    SUBTITLE_COLOR = "#ff6b6b"
