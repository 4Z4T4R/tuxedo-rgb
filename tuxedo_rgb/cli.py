#!/usr/bin/env python3
"""Command-line interface for Tuxedo RGB Keyboard Control"""

import argparse
import sys
import time
from .controller import TuxedoController
from .effects.basic import BasicEffects
from .effects.rainbow import RainbowEffects
from .effects.schemes import ColorSchemes


def parse_color(color_str):
    """Parse color string in format 'R,G,B' to tuple (r, g, b)"""
    try:
        r, g, b = map(int, color_str.split(','))
        if not all(0 <= c <= 255 for c in (r, g, b)):
            raise ValueError("Color values must be between 0 and 255")
        return (r, g, b)
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"Invalid color format: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Control Tuxedo RGB keyboard from command line"
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Solid color command
    solid_parser = subparsers.add_parser('solid', help='Set solid color')
    solid_parser.add_argument(
        'color',
        type=parse_color,
        help='RGB color in format R,G,B (e.g., 255,0,0 for red)'
    )

    # Breathing effect command
    breathing_parser = subparsers.add_parser('breathing', help='Breathing effect')
    breathing_parser.add_argument(
        'color',
        type=parse_color,
        help='RGB color in format R,G,B'
    )
    breathing_parser.add_argument(
        '--duration',
        type=float,
        default=3.0,
        help='Duration of one breath cycle in seconds (default: 3.0)'
    )

    # Rainbow static command
    subparsers.add_parser('rainbow-static', help='Static rainbow effect')

    # Rainbow wave command
    wave_parser = subparsers.add_parser('rainbow-wave', help='Rainbow wave effect')
    wave_parser.add_argument(
        '--duration',
        type=float,
        default=5.0,
        help='Duration of one wave cycle in seconds (default: 5.0)'
    )

    # Color cycle command
    cycle_parser = subparsers.add_parser('color-cycle', help='Color cycle effect')
    cycle_parser.add_argument(
        '--scheme',
        choices=list(ColorSchemes.SCHEMES.keys()),
        default='sunset',
        help='Color scheme to use (default: sunset)'
    )
    cycle_parser.add_argument(
        '--duration',
        type=float,
        default=5.0,
        help='Duration of one cycle in seconds (default: 5.0)'
    )

    # List schemes command
    subparsers.add_parser('list-schemes', help='List available color schemes')

    # Reset/cleanup command
    subparsers.add_parser('reset', help='Reset keyboard to white')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Handle list-schemes without requiring controller
    if args.command == 'list-schemes':
        print("Available color schemes:")
        for name in ColorSchemes.SCHEMES.keys():
            print(f"  - {name}")
        return 0

    # Initialize controller
    try:
        controller = TuxedoController()
        basic_effects = BasicEffects(controller)
        rainbow_effects = RainbowEffects(controller)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("\nNote: This tool requires:", file=sys.stderr)
        print("  1. A Tuxedo laptop with RGB keyboard", file=sys.stderr)
        print("  2. The tuxedo-keyboard kernel module loaded", file=sys.stderr)
        print("  3. Root/sudo privileges to access LED controls", file=sys.stderr)
        return 1

    try:
        if args.command == 'solid':
            print(f"Setting keyboard to color {args.color}")
            basic_effects.solid_color(*args.color)

        elif args.command == 'breathing':
            print(f"Starting breathing effect with color {args.color}")
            print("Press Ctrl+C to stop")
            basic_effects.breathing(args.color, duration=args.duration)

        elif args.command == 'rainbow-static':
            print("Setting static rainbow effect")
            rainbow_effects.rainbow_static()

        elif args.command == 'rainbow-wave':
            print("Starting rainbow wave effect")
            print("Press Ctrl+C to stop")
            rainbow_effects.rainbow_wave(duration=args.duration)

        elif args.command == 'color-cycle':
            print(f"Starting color cycle with {args.scheme} scheme")
            print("Press Ctrl+C to stop")
            rainbow_effects.color_cycle(scheme=args.scheme, duration=args.duration)

        elif args.command == 'reset':
            print("Resetting keyboard to white")
            controller.cleanup()

    except KeyboardInterrupt:
        print("\nStopping effect...")
        controller.cleanup()
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
