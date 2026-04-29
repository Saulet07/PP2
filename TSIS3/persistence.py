import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "red",
    "difficulty": "medium"
}


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                # Merge with defaults in case new keys added
                settings = DEFAULT_SETTINGS.copy()
                settings.update(data)
                return settings
        except Exception:
            pass
    return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)


def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return []


def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f, indent=2)


def add_score(name, score, distance):
    lb = load_leaderboard()
    lb.append({"name": name, "score": score, "distance": int(distance)})
    lb.sort(key=lambda x: x["score"], reverse=True)
    lb = lb[:10]
    save_leaderboard(lb)
    return lb