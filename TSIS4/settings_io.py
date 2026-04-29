"""
settings_io.py — load / save settings.json
"""
import json, os

SETTINGS_FILE = "settings.json"

DEFAULTS = {
    "snake_color": [0, 200, 80],
    "grid_overlay": True,
    "sound": True,
}


def load_settings() -> dict:
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE) as f:
                data = json.load(f)
            merged = DEFAULTS.copy()
            merged.update(data)
            return merged
        except Exception:
            pass
    return DEFAULTS.copy()


def save_settings(settings: dict):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)