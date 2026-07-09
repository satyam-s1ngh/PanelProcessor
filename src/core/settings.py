import json
from pathlib import Path


class Settings:
    CONFIG_PATH = Path.home() / "panel_processor_settings.json"

    def __init__(self):
        self.border_thickness = 0.0
        self.border_color = "#000000"

        self.corner_radius = 0.0

        self.shadow_enabled = False
        self.shadow_blur = 20
        self.shadow_opacity = 80
        self.shadow_offset_x = 0
        self.shadow_offset_y = 0
        self.shadow_color = "#000000"

        self.background_enabled = False
        self.background_color = "#ffffff"

        self.last_input_folder = ""
        self.last_output_folder = ""

    def to_dict(self):
        return {
            "border_thickness": self.border_thickness,
            "border_color": self.border_color,
            "corner_radius": self.corner_radius,

            "shadow_enabled": self.shadow_enabled,
            "shadow_blur": self.shadow_blur,
            "shadow_opacity": self.shadow_opacity,
            "shadow_offset_x": self.shadow_offset_x,
            "shadow_offset_y": self.shadow_offset_y,
            "shadow_color": self.shadow_color,

            "background_enabled": self.background_enabled,
            "background_color": self.background_color,

            "last_input_folder": self.last_input_folder,
            "last_output_folder": self.last_output_folder,
        }

    def load(self):
        if not self.CONFIG_PATH.exists():
            return

        try:
            data = json.loads(self.CONFIG_PATH.read_text())

            for key, value in data.items():
                if hasattr(self, key):
                    setattr(self, key, value)

        except Exception:
            pass

    def save(self):
        try:
            self.CONFIG_PATH.write_text(
                json.dumps(
                    self.to_dict(),
                    indent=4,
                )
            )
        except Exception:
            pass