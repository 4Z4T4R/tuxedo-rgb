from typing import Tuple
import time
import math
from ..controller import TuxedoController


class BasicEffects:
    def __init__(self, controller: TuxedoController):
        self.controller = controller

    def solid_color(self, r: int, g: int, b: int) -> None:
        """Set entire keyboard to a single color"""
        self.controller.set_all_zones(r, g, b)

    def breathing(self, color: Tuple[int, int, int], duration: float = 3.0, steps: int = 50) -> None:
        """
        Create a breathing effect that pulses a single color

        Args:
            color: RGB color tuple
            duration: Time for one breath cycle in seconds
            steps: Number of steps in the animation
        """
        try:
            sleep_time = duration / steps
            while True:
                for i in range(steps):
                    # Use sine wave for smooth breathing
                    scale = (math.sin(i * 2 * math.pi / steps) + 1) / 2
                    r = int(color[0] * scale)
                    g = int(color[1] * scale)
                    b = int(color[2] * scale)
                    self.controller.set_all_zones(r, g, b)
                    time.sleep(sleep_time)

        except KeyboardInterrupt:
            self.controller.cleanup()