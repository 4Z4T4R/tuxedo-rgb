"""Tuxedo RGB Keyboard Control

A GTK4-based GUI application for controlling RGB keyboard backlighting
on Tuxedo laptops.
"""

__version__ = "0.1.0"
__author__ = "Tuxedo RGB Contributors"

from .controller import TuxedoController

__all__ = ["TuxedoController"]

# Make GUI imports optional (requires GTK4)
try:
    from .gui import TuxedoRGBApplication, main
    __all__.extend(["TuxedoRGBApplication", "main"])
except ImportError:
    # GTK4 not available, GUI functionality disabled
    pass
