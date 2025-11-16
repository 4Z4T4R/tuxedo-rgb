# tuxedo_rgb/effects/schemes.py

class ColorSchemes:
    """Predefined color schemes for RGB effects"""

    SCHEMES = {
        'sunset': [(1, 0, 0), (1, 0.5, 0), (1, 0, 0.5)],  # Red -> Orange -> Pink
        'ocean': [(0, 0.5, 1), (0, 1, 0.8), (0, 0.8, 1)],  # Blue -> Cyan variations
        'forest': [(0, 0.8, 0), (0.5, 0.8, 0), (0, 0.6, 0)],  # Green variations
        'purple_gold': [(0.5, 0, 1), (1, 0.8, 0), (0.8, 0, 1)],  # Purple -> Gold -> Purple
        'cyberpunk': [(0, 1, 1), (1, 0, 1), (1, 1, 0)]  # Cyan -> Magenta -> Yellow
    }

    @classmethod
    def get_scheme(cls, name: str) -> list:
        """Get color scheme by name"""
        if name not in cls.SCHEMES:
            raise ValueError(
                f"Unknown color scheme: {name}. "
                f"Available schemes: {', '.join(cls.SCHEMES.keys())}"
            )
        return cls.SCHEMES[name]