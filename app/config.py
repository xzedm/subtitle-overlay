import json
import os
from pathlib import Path
from typing import Any, Dict

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / '.subtitle_overlay'
        self.config_file = self.config_dir / 'config.json'
        self.config_dir.mkdir(exist_ok=True)
        self.settings = self.load_settings()
    
    def get_default_settings(self) -> Dict[str, Any]:
        return {
            'window': {
                'x': 100,
                'y': 100,
                'width': 800,
                'height': 100,
                'opacity': 0.85,
                'always_on_top': True
            },
            'text': {
                'font_family': 'Arial',
                'font_size': 22,
                'color': '#FFFFFF',
                'outline': True,
                'outline_color': '#000000',
                'outline_width': 2
            },
            'background': {
                'color': '#000000',
                'opacity': 0.85
            },
            'behavior': {
                'auto_hide': True,
                'auto_hide_delay': 4000,  # milliseconds
                'max_lines': 3
            },
            'server': {
                'port': 8765,
                'host': '127.0.0.1'
            }
        }
    
    def load_settings(self) -> Dict[str, Any]:
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    defaults = self.get_default_settings()
                    # Merge with defaults to handle new settings
                    return {**defaults, **loaded}
            except Exception as e:
                print(f"Error loading config: {e}")
        return self.get_default_settings()
    
    def save_settings(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, *keys):
        value = self.settings
        for key in keys:
            value = value.get(key)
            if value is None:
                return None
        return value
    
    def set(self, *keys, value):
        settings = self.settings
        for key in keys[:-1]:
            settings = settings.setdefault(key, {})
        settings[keys[-1]] = value
        self.save_settings()