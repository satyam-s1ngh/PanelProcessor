from dataclasses import dataclass


@dataclass
class Settings:
    def __init__(self):
        self.border_thickness = 0.0
        self.border_color = "black"
        self.corner_radius: float = 0.0
        self.shadow_enabled = False
        self.shadow_blur = 20
        self.shadow_opacity = 120
        self.shadow_offset_x = 0
        self.shadow_offset_y = 0
        self.shadow_color = "#000000"
        