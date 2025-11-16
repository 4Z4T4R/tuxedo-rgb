# tuxedo_rgb/effects/rainbow.py

import time
import colorsys
from typing import Optional
from ..controller import TuxedoController
from .schemes import ColorSchemes


class RainbowEffects:
    def __init__(self, controller: TuxedoController):
        self.controller = controller

    def rainbow_static(self) -> None:
        """Create a static rainbow effect across the keyboard"""
        colors = [
            colorsys.hsv_to_rgb(h / 3.0, 1.0, 1.0)
            for h in range(3)
        ]

        # Convert to RGB values (0-255)
        colors = [(int(r * 255), int(g * 255), int(b * 255)) for r, g, b in colors]

        self.controller.set_zone_color('left', *colors[0])
        self.controller.set_zone_color('center', *colors[1])
        self.controller.set_zone_color('right', *colors[2])

    def rainbow_wave(self, duration: float = 5, steps: int = 100) -> None:
        """
        Create a smooth rainbow wave effect

        Args:
            duration: Time for one complete cycle in seconds
            steps: Number of steps in the animation
        """
        try:
            sleep_time = duration / steps
            while True:
                for i in range(steps):
                    hue = (i / steps) % 1.0

                    # Calculate three colors spaced evenly around the color wheel
                    color1 = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                    color2 = colorsys.hsv_to_rgb((hue + 0.33) % 1.0, 1.0, 1.0)
                    color3 = colorsys.hsv_to_rgb((hue + 0.66) % 1.0, 1.0, 1.0)

                    # Convert to RGB values (0-255)
                    color1 = tuple(int(c * 255) for c in color1)
                    color2 = tuple(int(c * 255) for c in color2)
                    color3 = tuple(int(c * 255) for c in color3)

                    self.controller.set_zone_color('left', *color1)
                    self.controller.set_zone_color('center', *color2)
                    self.controller.set_zone_color('right', *color3)
                    time.sleep(sleep_time)

        except KeyboardInterrupt:
            self.controller.cleanup()

    def color_cycle(self, scheme: str = 'sunset', duration: float = 5, steps: int = 100) -> None:
        """
        Cycle through colors in a specific color scheme

        Args:
            scheme: Name of the color scheme to use
            duration: Time for one complete cycle in seconds
            steps: Number of steps in the animation
        """
        colors = ColorSchemes.get_scheme(scheme)

        try:
            sleep_time = duration / steps
            while True:
                for i in range(steps):
                    pos = i / steps
                    num_colors = len(colors)

                    idx1 = int(pos * num_colors)
                    idx2 = (idx1 + 1) % num_colors

                    local_pos = (pos * num_colors) % 1.0

                    color1 = colors[idx1]
                    color2 = colors[idx2]

                    # Interpolate between colors
                    current_color = tuple(
                        c1 * (1 - local_pos) + c2 * local_pos
                        for c1, c2 in zip(color1, color2)
                    )

                    # Convert to RGB values (0-255)
                    rgb = tuple(int(c * 255) for c in current_color)
                    self.controller.set_all_zones(*rgb)
                    time.sleep(sleep_time)

        except KeyboardInterrupt:
            self.controller.cleanup()