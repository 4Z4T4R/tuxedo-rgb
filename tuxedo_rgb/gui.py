#!/usr/bin/env python3
import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Gdk
import threading
from typing import Optional

from .controller import TuxedoController
from .effects.basic import BasicEffects
from .effects.rainbow import RainbowEffects
from .effects.schemes import ColorSchemes


class TuxedoRGBWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize controllers and effects
        self.controller = TuxedoController()
        self.basic_effects = BasicEffects(self.controller)
        self.rainbow_effects = RainbowEffects(self.controller)

        # Keep track of running effect thread
        self.effect_thread: Optional[threading.Thread] = None
        self.stop_effect = threading.Event()

        # Window setup
        self.set_title("Tuxedo RGB Control")
        self.set_default_size(600, 400)

        # Create main layout
        self.setup_ui()

    def setup_ui(self):
        """Create and setup all UI elements"""
        # Main container with padding
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        self.set_child(main_box)

        # Header section
        header_label = Gtk.Label()
        header_label.set_markup("<b>Tuxedo RGB Keyboard Control</b>")
        main_box.append(header_label)

        # Color picker section
        color_section = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        color_label = Gtk.Label(label="Static Color:")
        self.color_button = Gtk.ColorButton()
        self.color_button.set_rgba(Gdk.RGBA(1, 1, 1, 1))  # Default to white
        self.color_button.connect('color-set', self.on_color_changed)
        color_section.append(color_label)
        color_section.append(self.color_button)
        main_box.append(color_section)

        # Effects section
        effects_section = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        effects_label = Gtk.Label(label="Effect:")
        self.effects_combo = Gtk.ComboBoxText()
        self.effects = [
            "Solid Color",
            "Breathing",
            "Rainbow Static",
            "Rainbow Wave",
            "Color Cycle"
        ]
        for effect in self.effects:
            self.effects_combo.append_text(effect)
        self.effects_combo.set_active(0)
        self.effects_combo.connect('changed', self.on_effect_changed)
        effects_section.append(effects_label)
        effects_section.append(self.effects_combo)
        main_box.append(effects_section)

        # Color scheme section
        scheme_section = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        scheme_label = Gtk.Label(label="Color Scheme:")
        self.scheme_combo = Gtk.ComboBoxText()
        for scheme in ColorSchemes.SCHEMES.keys():
            self.scheme_combo.append_text(scheme)
        self.scheme_combo.set_active(0)
        scheme_section.append(scheme_label)
        scheme_section.append(self.scheme_combo)
        main_box.append(scheme_section)

        # Duration section
        duration_section = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        duration_label = Gtk.Label(label="Effect Duration (seconds):")
        self.duration_scale = Gtk.Scale()
        self.duration_scale.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.duration_scale.set_range(1, 10)
        self.duration_scale.set_value(5)
        self.duration_scale.set_digits(1)
        self.duration_scale.set_draw_value(True)
        duration_section.append(duration_label)
        duration_section.append(self.duration_scale)
        main_box.append(duration_section)

        # Buttons section
        buttons_section = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        self.apply_button = Gtk.Button(label="Apply Effect")
        self.apply_button.connect('clicked', self.on_apply_clicked)

        self.stop_button = Gtk.Button(label="Stop Effect")
        self.stop_button.connect('clicked', self.on_stop_clicked)
        self.stop_button.set_sensitive(False)

        buttons_section.append(self.apply_button)
        buttons_section.append(self.stop_button)
        main_box.append(buttons_section)

    def on_color_changed(self, button):
        """Handle color picker changes"""
        rgba = button.get_rgba()
        r = int(rgba.red * 255)
        g = int(rgba.green * 255)
        b = int(rgba.blue * 255)
        self.controller.set_all_zones(r, g, b)

    def on_effect_changed(self, combo):
        """Handle effect selection changes"""
        effect = self.effects[combo.get_active()]
        # Enable/disable relevant controls based on effect
        uses_scheme = effect in ["Color Cycle"]
        self.scheme_combo.set_sensitive(uses_scheme)

        uses_duration = effect in ["Breathing", "Rainbow Wave", "Color Cycle"]
        self.duration_scale.set_sensitive(uses_duration)

    def stop_current_effect(self):
        """Stop any running effect thread"""
        if self.effect_thread and self.effect_thread.is_alive():
            self.stop_effect.set()
            self.effect_thread.join()
            self.stop_effect.clear()

    def on_stop_clicked(self, button):
        """Handle stop button clicks"""
        self.stop_current_effect()
        self.controller.cleanup()
        self.apply_button.set_sensitive(True)
        self.stop_button.set_sensitive(False)

    def run_effect(self, effect_func, *args, **kwargs):
        """Run an effect in a separate thread"""
        try:
            while not self.stop_effect.is_set():
                effect_func(*args, **kwargs)
        except Exception as e:
            print(f"Effect error: {e}")
        finally:
            GLib.idle_add(self.on_effect_complete)

    def on_effect_complete(self):
        """Called when an effect completes or is stopped"""
        self.apply_button.set_sensitive(True)
        self.stop_button.set_sensitive(False)
        return False

    def on_apply_clicked(self, button):
        """Handle apply button clicks"""
        self.stop_current_effect()

        effect = self.effects[self.effects_combo.get_active()]
        duration = self.duration_scale.get_value()

        # Start the selected effect
        if effect == "Solid Color":
            rgba = self.color_button.get_rgba()
            self.controller.set_all_zones(
                int(rgba.red * 255),
                int(rgba.green * 255),
                int(rgba.blue * 255)
            )
        else:
            self.apply_button.set_sensitive(False)
            self.stop_button.set_sensitive(True)

            if effect == "Rainbow Static":
                self.effect_thread = threading.Thread(
                    target=self.run_effect,
                    args=(self.rainbow_effects.rainbow_static,)
                )
            elif effect == "Rainbow Wave":
                self.effect_thread = threading.Thread(
                    target=self.run_effect,
                    args=(self.rainbow_effects.rainbow_wave,),
                    kwargs={'duration': duration}
                )
            elif effect == "Color Cycle":
                scheme = self.scheme_combo.get_active_text()
                self.effect_thread = threading.Thread(
                    target=self.run_effect,
                    args=(self.rainbow_effects.color_cycle,),
                    kwargs={'scheme': scheme, 'duration': duration}
                )
            elif effect == "Breathing":
                rgba = self.color_button.get_rgba()
                color = (
                    int(rgba.red * 255),
                    int(rgba.green * 255),
                    int(rgba.blue * 255)
                )
                self.effect_thread = threading.Thread(
                    target=self.run_effect,
                    args=(self.basic_effects.breathing,),
                    kwargs={'color': color, 'duration': duration}
                )

            self.effect_thread.start()


class TuxedoRGBApplication(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='org.tuxedo.rgb')

    def do_activate(self):
        win = TuxedoRGBWindow(application=self)
        win.present()


def main():
    app = TuxedoRGBApplication()
    return app.run(None)


if __name__ == '__main__':
    main()