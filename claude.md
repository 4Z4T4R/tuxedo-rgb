# Tuxedo RGB Keyboard Control

## Project Overview

This project provides a GTK4-based GUI application for controlling RGB keyboard backlighting on Tuxedo laptops running Ubuntu/Linux. It allows users to customize their keyboard appearance with various color themes, patterns, and animated effects.

## Architecture

### Core Components

1. **TuxedoController** (`tuxedo_rgb/controller.py`)
   - Interfaces with the keyboard hardware via Linux sysfs
   - Controls 3 keyboard zones: left, center, right
   - Expects tuxedo-keyboard kernel module to be loaded
   - Hardware uses GRB color order (not standard RGB)

2. **GUI** (`tuxedo_rgb/gui.py`)
   - GTK4-based graphical interface
   - Multi-threaded effect execution
   - Real-time color picker and effect controls
   - Responsive UI with enable/disable states

3. **Effects System** (`tuxedo_rgb/effects/`)
   - **BasicEffects**: Solid colors and breathing effect
   - **RainbowEffects**: Rainbow static, wave, and color cycling
   - **ColorSchemes**: Predefined color palettes

### LED Control Paths

The controller uses sysfs to communicate with the keyboard:
- Left zone: `/sys/class/leds/rgb:kbd_backlight/multi_intensity`
- Center zone: `/sys/class/leds/rgb:kbd_backlight_1/multi_intensity`
- Right zone: `/sys/class/leds/rgb:kbd_backlight_2/multi_intensity`

## Available Effects

1. **Solid Color** - Set entire keyboard to a single static color
2. **Breathing** - Smooth pulsing effect with selected color
3. **Rainbow Static** - Static rainbow across three zones
4. **Rainbow Wave** - Animated rainbow that cycles smoothly
5. **Color Cycle** - Cycles through a themed color scheme

## Color Schemes

- **sunset**: Red → Orange → Pink
- **ocean**: Blue and cyan variations
- **forest**: Green variations
- **purple_gold**: Purple → Gold → Purple
- **cyberpunk**: Cyan → Magenta → Yellow

## Technical Details

### Threading Model
- Main thread handles GTK UI
- Effect threads run animations in background
- Thread-safe stop mechanism using threading.Event
- GLib.idle_add for UI updates from threads

### Hardware Quirks
- Tuxedo keyboards expect GRB order (Green, Red, Blue) not RGB
- Requires root/sudo access to write to sysfs paths
- Requires tuxedo-keyboard kernel module loaded

## Dependencies

- Python 3.8+
- GTK4 (PyGObject)
- tuxedo-keyboard kernel module

## Development Notes

### Adding New Effects
1. Create effect method in appropriate class (BasicEffects or RainbowEffects)
2. Add effect name to GUI effects list
3. Wire up effect in on_apply_clicked handler
4. Update on_effect_changed if special controls needed

### Adding New Color Schemes
Add new entry to ColorSchemes.SCHEMES dictionary with normalized RGB values (0.0-1.0)

## Security Considerations

The application requires elevated privileges to write to sysfs. On production systems:
1. Use udev rules to grant appropriate permissions
2. Or run application with sudo
3. Consider creating a systemd service with proper capabilities

## Future Enhancements

- Per-key RGB control (if hardware supports)
- Save/load custom profiles
- Startup effect configuration
- More complex multi-zone patterns
- Brightness control
- Integration with system themes
