import json
from os import path


def _load_settings():
    if not path.exists("settings.json"):
        with open("settings.json", "w") as f:
            json.dump({"sounds": {"music_volume": 0.5, "sfx_volume": 0.5}}, f)
    with open("settings.json", "r") as f:
        return json.load(f)

class Settings:
    settings = _load_settings()

    @staticmethod
    def get_music_volume():
        return Settings.settings["sounds"]["music_volume"]
    
    @staticmethod
    def get_sfx_volume():
        return Settings.settings["sounds"]["sfx_volume"]
    
    @staticmethod
    def set_music_volume(volume: float):
        Settings.settings["sounds"]["music_volume"] = volume
    
    @staticmethod
    def set_sfx_volume(volume: float):
        Settings.settings["sounds"]["sfx_volume"] = volume
        
    @staticmethod
    def save_settings():
        with open("settings.json", "w") as f:
            json.dump(Settings.settings, f)