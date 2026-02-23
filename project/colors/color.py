from enum import Enum
from typing import Dict, Set, List


class ColorName(str, Enum):
    """Enumeration of all supported color names."""
    BLACK = "black"
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    MAGENTA = "magenta"
    CYAN = "cyan"
    WHITE = "white"
    BRIGHT_BLACK = "bright_black"
    BRIGHT_RED = "bright_red"
    BRIGHT_GREEN = "bright_green"
    BRIGHT_YELLOW = "bright_yellow"
    BRIGHT_BLUE = "bright_blue"
    BRIGHT_MAGENTA = "bright_magenta"
    BRIGHT_CYAN = "bright_cyan"
    BRIGHT_WHITE = "bright_white"
    GREY = "grey"
    GRAY = "gray"
    LIGHT_RED = "light_red"
    LIGHT_GREEN = "light_green"
    LIGHT_YELLOW = "light_yellow"
    LIGHT_BLUE = "light_blue"
    LIGHT_MAGENTA = "light_magenta"
    LIGHT_CYAN = "light_cyan"
    LIGHT_WHITE = "light_white"


class Colors:
    """Professional color handling for the maze application."""

    _ANSI_CODES: Dict[ColorName, int] = {
        ColorName.BLACK: 30,
        ColorName.RED: 31,
        ColorName.GREEN: 32,
        ColorName.YELLOW: 33,
        ColorName.BLUE: 34,
        ColorName.MAGENTA: 35,
        ColorName.CYAN: 36,
        ColorName.WHITE: 37,
        ColorName.BRIGHT_BLACK: 90,
        ColorName.BRIGHT_RED: 91,
        ColorName.BRIGHT_GREEN: 92,
        ColorName.BRIGHT_YELLOW: 93,
        ColorName.BRIGHT_BLUE: 94,
        ColorName.BRIGHT_MAGENTA: 95,
        ColorName.BRIGHT_CYAN: 96,
        ColorName.BRIGHT_WHITE: 97,
        ColorName.GREY: 90,
        ColorName.GRAY: 90,
        ColorName.LIGHT_RED: 91,
        ColorName.LIGHT_GREEN: 92,
        ColorName.LIGHT_YELLOW: 93,
        ColorName.LIGHT_BLUE: 94,
        ColorName.LIGHT_MAGENTA: 95,
        ColorName.LIGHT_CYAN: 96,
        ColorName.LIGHT_WHITE: 97,
    }

    _VALID_COLORS: Set[ColorName] = set(_ANSI_CODES.keys())

    FORBIDDEN_WALL_FLAG: Set[ColorName] = {ColorName.BLACK}

    @classmethod
    def get_ansi_code(cls, color_name: str) -> int:
        """Get ANSI color code for a color name."""
        try:
            color_enum = ColorName(color_name.lower())
            return cls._ANSI_CODES.get(color_enum, 37)
        except ValueError:
            return 37

    @classmethod
    def get_ansi_escape(cls, color_name: str) -> str:
        """Get ANSI escape sequence for a color name."""
        return f"\033[{cls.get_ansi_code(color_name)}m"

    @classmethod
    def get_reset_escape(cls) -> str:
        """Get ANSI reset escape sequence."""
        return "\033[0m"

    @classmethod
    def is_valid_color(cls, color_name: str) -> bool:
        """Check if a color name is valid."""
        try:
            color_enum = ColorName(color_name.lower())
            return color_enum in cls._VALID_COLORS
        except ValueError:
            return False

    @classmethod
    def get_available_colors(cls) -> List[str]:
        """Get list of all available color names."""
        return [color.value for color in ColorName]

    @classmethod
    def get_complementary_ansi_code(cls, color_name: str) -> int:
        """Get a complementary ANSI color code."""
        base_code = cls.get_ansi_code(color_name)
        base_index = base_code % 10
        opposite_index = (base_index + 4) % 8
        return (90 if base_code >= 90 else 30) + opposite_index

    @classmethod
    def get_complementary_escape(cls, color_name: str) -> str:
        """Get ANSI escape sequence for a complementary color."""
        return f"\033[{cls.get_complementary_ansi_code(color_name)}m"

    @classmethod
    def are_colors_different(cls, color1: str, color2: str) -> bool:
        """Check if two colors are different."""
        return color1.lower() != color2.lower()

    @classmethod
    def is_forbidden_for_wall_flag(cls, color_name: str) -> bool:
        """Check if a color is forbidden for wall/flag colors."""
        try:
            color_enum = ColorName(color_name.lower())
            return color_enum in cls.FORBIDDEN_WALL_FLAG
        except ValueError:
            return True