# Development Guide

## Quick Start with Conda

### 1. Create and Activate Conda Environment

```bash
cd ~/Engineering/tuxedo-rgb

# Create the conda environment from the environment.yml file
conda env create -f environment.yml

# Activate the environment
conda activate tuxedo-rgb
```

### 2. Test the Installation

```bash
# Test CLI
python -m tuxedo_rgb.cli list-schemes

# Test with actual hardware (requires sudo)
sudo $(which python) -m tuxedo_rgb.cli solid 255,0,0

# Launch GUI (requires sudo)
sudo $(which python) -m tuxedo_rgb.gui
```

### 3. Making Changes

The package is installed in editable mode (`-e`), so any changes you make to the source code will be immediately available without reinstalling.

### 4. Deactivate Environment

```bash
conda deactivate
```

## Installing System GTK4 Dependencies

If PyGObject can't find GTK4, you may need to install system packages:

```bash
sudo apt update
sudo apt install libgtk-4-1 gir1.2-gtk-4.0 gobject-introspection libgirepository1.0-dev
```

## Alternative: Manual Conda Setup

If the environment.yml doesn't work, set up manually:

```bash
# Create environment
conda create -n tuxedo-rgb python=3.11

# Activate
conda activate tuxedo-rgb

# Install dependencies
conda install -c conda-forge pygobject gtk4

# Install package in development mode
pip install -e .
```

## Creating a Debian Package

Once development is complete, we can create a proper `.deb` package for native installation.

### Prerequisites

```bash
sudo apt install debhelper dh-python python3-all python3-setuptools
```

### Build Process

```bash
# Create debian packaging structure
mkdir -p debian

# Build the package
dpkg-buildpackage -us -uc

# Install the resulting .deb
sudo dpkg -i ../tuxedo-rgb_*.deb
```

### Package Installation

Once we have the `.deb` package:

```bash
sudo dpkg -i tuxedo-rgb_0.1.0_all.deb
sudo apt-get install -f  # Fix any missing dependencies
```

After installation via `.deb`, users can run:

```bash
sudo tuxedo-rgb        # GUI
sudo tuxedo-rgb-cli    # CLI
```

## Testing Without Tuxedo Hardware

For development without actual Tuxedo hardware, you can mock the sysfs paths:

```bash
# Create mock LED paths
sudo mkdir -p /sys/class/leds/rgb:kbd_backlight
sudo mkdir -p /sys/class/leds/rgb:kbd_backlight_1
sudo mkdir -p /sys/class/leds/rgb:kbd_backlight_2

# Create mock control files
for i in "" "_1" "_2"; do
    sudo touch /sys/class/leds/rgb:kbd_backlight${i}/multi_intensity
    sudo chmod 666 /sys/class/leds/rgb:kbd_backlight${i}/multi_intensity
done
```

## Project Structure

```
tuxedo-rgb/
├── tuxedo_rgb/           # Main package
│   ├── __init__.py
│   ├── gui.py            # GTK4 GUI
│   ├── controller.py     # Hardware interface
│   ├── cli.py            # Command-line interface
│   └── effects/          # RGB effects
│       ├── __init__.py
│       ├── basic.py
│       ├── rainbow.py
│       └── schemes.py
├── scripts/
│   └── tuxedo-rgb        # Entry point
├── debian/               # Debian packaging (to be created)
├── environment.yml       # Conda environment
├── setup.py              # Python package config
├── requirements.txt      # Pip dependencies
├── README.md             # User documentation
├── TESTING.md            # Testing guide
└── DEVELOPMENT.md        # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly (see TESTING.md)
5. Submit a pull request

## Code Style

- Follow PEP 8
- Use type hints where appropriate
- Document all public methods and classes
- Keep functions focused and small

## Adding New Features

### Adding a New Effect

1. Create the effect method in `tuxedo_rgb/effects/basic.py` or `rainbow.py`
2. Add the effect to the GUI in `tuxedo_rgb/gui.py`:
   - Add to `self.effects` list
   - Add handler in `on_apply_clicked`
   - Update `on_effect_changed` for special controls
3. Add CLI support in `tuxedo_rgb/cli.py`
4. Update documentation

### Adding a New Color Scheme

Edit `tuxedo_rgb/effects/schemes.py` and add to the `SCHEMES` dictionary:

```python
'my_scheme': [(1, 0, 0), (0, 1, 0), (0, 0, 1)]  # Red, Green, Blue
```

Values should be normalized RGB (0.0-1.0).

## Roadmap to Native Package

- [x] Conda development environment
- [ ] Create debian/ packaging structure
- [ ] Write debian/control file
- [ ] Write debian/rules file
- [ ] Test .deb build process
- [ ] Create installation scripts
- [ ] Set up udev rules in package
- [ ] Create systemd service (optional)
- [ ] Test on clean Ubuntu installation
