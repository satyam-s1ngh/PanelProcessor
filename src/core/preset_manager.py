import json
from pathlib import Path


class PresetManager:
    PRESET_PATH = Path.home() / "panel_processor_presets.json"

    def __init__(self):
        self.presets = {}
        self.load()

    def load(self):
        if not self.PRESET_PATH.exists():
            self.presets = {}
            return

        try:
            self.presets = json.loads(
                self.PRESET_PATH.read_text()
            )
        except Exception:
            self.presets = {}

    def save(self):
        try:
            self.PRESET_PATH.write_text(
                json.dumps(
                    self.presets,
                    indent=4,
                )
            )
        except Exception:
            pass

    def get_names(self):
        return sorted(self.presets.keys())

    def get_preset(self, name):
        return self.presets.get(name)

    def save_preset(self, name, settings_data):
        self.presets[name] = settings_data
        self.save()

    def delete_preset(self, name):
        if name in self.presets:
            del self.presets[name]
            self.save()