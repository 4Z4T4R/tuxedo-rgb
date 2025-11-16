from pathlib import Path
import time
from typing import Dict, Tuple, Optional
import colorsys


class TuxedoController:
    """Core controller for Tuxedo keyboard RGB functionality"""

    def __init__(self):
        # Initialize LED paths using sysfs
        self.zones = {
            'left': Path("/sys/class/leds/rgb:kbd_backlight"),
            'center': Path("/sys/class/leds/rgb:kbd_backlight_1"),
            'right': Path("/sys/class/leds/rgb:kbd_backlight_2")
        }
        self.verify_paths()

    def verify_paths(self) -> None:
        """Verify all required LED control paths exist"""
        for zone, path in self.zones.items():
            if not (path / "multi_intensity").exists():
                raise RuntimeError(
                    f"Required path {path}/multi_intensity does not exist. "
                    "Please ensure the tuxedo-keyboard module is loaded."
                )

    def set_zone_color(self, zone: str, r: int, g: int, b: int) -> None:
        """
        Set RGB color for a specific keyboard zone

        Args:
            zone: Keyboard zone ('left', 'center', 'right')
            r, g, b: RGB color values (0-255)
        """
        if zone not in self.zones:
            raise ValueError(f"Invalid zone: {zone}")

        path = self.zones[zone]
        color_str = f"{g} {r} {b}"  # Note: Hardware expects GRB order

        try:
            (path / "multi_intensity").write_text(color_str)
        except (IOError, OSError) as e:
            raise RuntimeError(f"Failed to set color for {zone} zone: {e}")

    def set_all_zones(self, r: int, g: int, b: int) -> None:
        """Set all keyboard zones to the same RGB color"""
        for zone in self.zones:
            self.set_zone_color(zone, r, g, b)

    def cleanup(self) -> None:
        """Reset keyboard to neutral state (white)"""
        self.set_all_zones(255, 255, 255)