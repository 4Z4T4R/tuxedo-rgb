# Testing Guide for Tuxedo RGB Keyboard Control

## Quick Start Testing

Once you're on your Tuxedo laptop, follow these steps to test the application:

### 1. Install System Dependencies

```bash
sudo apt update
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 python3-pip
```

### 2. Verify Tuxedo Keyboard Module

Check that the tuxedo-keyboard module is loaded:

```bash
lsmod | grep tuxedo
```

Expected output should show `tuxedo_keyboard` and related modules.

Verify LED paths exist:

```bash
ls /sys/class/leds/ | grep kbd_backlight
```

You should see:
- `rgb:kbd_backlight`
- `rgb:kbd_backlight_1`
- `rgb:kbd_backlight_2`

### 3. Install the Application

**Option A: Using Conda (Recommended)**

```bash
cd ~/Engineering/tuxedo-rgb
conda env create -f environment.yml
conda activate tuxedo-rgb
```

**Option B: Using Virtual Environment**

```bash
cd ~/Engineering/tuxedo-rgb
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

**Option C: Using pipx**

```bash
cd ~/Engineering/tuxedo-rgb
pipx install -e .
```

### 4. Test with CLI (Quick Test)

The CLI is great for quick testing without needing the GUI:

**If using Conda:**

```bash
# Make sure conda environment is activated
conda activate tuxedo-rgb

# List available color schemes (no sudo needed)
python -m tuxedo_rgb.cli list-schemes

# Set keyboard to red (needs sudo)
sudo $(which python) -m tuxedo_rgb.cli solid 255,0,0

# Set keyboard to blue
sudo $(which python) -m tuxedo_rgb.cli solid 0,0,255

# Try breathing effect (press Ctrl+C to stop)
sudo $(which python) -m tuxedo_rgb.cli breathing 0,255,0 --duration 3

# Try rainbow wave (press Ctrl+C to stop)
sudo $(which python) -m tuxedo_rgb.cli rainbow-wave --duration 5

# Try color cycle with cyberpunk scheme (press Ctrl+C to stop)
sudo $(which python) -m tuxedo_rgb.cli color-cycle --scheme cyberpunk --duration 5

# Reset to white
sudo $(which python) -m tuxedo_rgb.cli reset
```

**If using venv:**

```bash
# Make sure venv is activated
source venv/bin/activate

# List available color schemes (no sudo needed)
python -m tuxedo_rgb.cli list-schemes

# Set keyboard to red (needs sudo with full path)
sudo venv/bin/python -m tuxedo_rgb.cli solid 255,0,0

# Other commands follow the same pattern
sudo venv/bin/python -m tuxedo_rgb.cli rainbow-wave --duration 5
```

### 5. Test the GUI

Launch the GUI application:

**If using Conda:**

```bash
conda activate tuxedo-rgb
sudo $(which python) -m tuxedo_rgb.gui
```

**If using venv:**

```bash
source venv/bin/activate
sudo venv/bin/python -m tuxedo_rgb.gui
```

**If installed via pipx:**

```bash
sudo $(which tuxedo-rgb)
```

#### GUI Testing Checklist

- [ ] Application window opens without errors
- [ ] Color picker responds to clicks
- [ ] Can select different effects from dropdown
- [ ] Can select different color schemes
- [ ] Duration slider works
- [ ] Apply button starts effects
- [ ] Stop button stops effects
- [ ] Solid color effect works
- [ ] Breathing effect works
- [ ] Rainbow static effect works
- [ ] Rainbow wave effect works
- [ ] Color cycle effect works with each scheme

## Troubleshooting During Testing

### Permission Denied Errors

If you see permission errors:

```bash
# Temporarily test with sudo
sudo python3 -m tuxedo_rgb.cli solid 255,0,0
```

For permanent solution without sudo, see README.md section on udev rules.

### LED Paths Not Found

If the application can't find LED paths:

1. Check if module is loaded:
   ```bash
   sudo modprobe tuxedo_keyboard
   ```

2. Check kernel messages:
   ```bash
   dmesg | grep -i tuxedo
   ```

3. Verify your laptop model is supported by tuxedo-keyboard

### GTK Import Errors

If you get GTK-related errors:

```bash
# Reinstall GTK4 dependencies
sudo apt install --reinstall gir1.2-gtk-4.0 python3-gi python3-gi-cairo
```

### Effect Doesn't Stop

If an effect keeps running after clicking Stop:
- Close the application window
- Run the reset command: `sudo python3 -m tuxedo_rgb.cli reset`

## Expected Behavior

### Solid Color
- All three zones (left, center, right) should show the selected color immediately
- No animation or flickering

### Breathing
- Keyboard should smoothly pulse between dim and bright
- Uses a sine wave for natural breathing rhythm
- Press Stop to end

### Rainbow Static
- Left, center, and right zones show different colors
- Colors should be from the rainbow spectrum
- Static (no animation)

### Rainbow Wave
- Smooth color transition across all zones
- Continuous loop until stopped
- Colors cycle through the rainbow spectrum

### Color Cycle
- All zones show the same color at once
- Smoothly transitions between colors in the selected scheme
- Continuous loop until stopped

## Performance Notes

- Effects run in separate threads to keep UI responsive
- Typical refresh rate: 20-100 fps depending on duration settings
- CPU usage should be minimal (< 5%)
- No noticeable lag when changing colors

## Known Limitations

- Only 3-zone control (left, center, right)
- No per-key RGB control
- Requires root/sudo for sysfs access
- Hardware limitation: GRB color order instead of RGB

## Reporting Issues

If you encounter issues during testing:

1. Note your laptop model
2. Check `dmesg` output for errors
3. Verify tuxedo-keyboard module version
4. Include any error messages
5. Note which specific effect/feature fails

Happy testing!
