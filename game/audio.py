import pygame as pg
import json
from os import path
import random
import numpy as np

# Check if the settings.json file exists
if not path.exists("settings.json"):
    with open("settings.json", "w") as f:
        json.dump({"sounds": {"music_volume": 0.5, "sfx_volume": 0.5}}, f)

# Load the settings.json file
with open("settings.json", "r") as f:
    settings = json.load(f)

class SFXAudio:
    def __init__(self, sound_path: str, volume: float = 1, pitch_shift_sigma: float = 1, pitch_shift_cap: float = 1.5):
        self.pitch_shift_sigma = pitch_shift_sigma
        self.pitch_shift_cap = pitch_shift_cap
        self.sound = pg.mixer.Sound(sound_path)
        self.sound.set_volume(settings["sounds"]["sfx_volume"]*volume)
        self.volume = settings["sounds"]["sfx_volume"]*volume
        
    def play(self):
        
        if self.pitch_shift_sigma == 0: 
            self.sound.play()
            return
        
        shift = random.gauss(0, self.pitch_shift_sigma)
        if abs(shift) > self.pitch_shift_cap:
            shift = self.pitch_shift_cap * np.sign(shift)
        
        new_sound = self._apply_pitch_shift(shift)
        new_sound.set_volume(self.volume)
        new_sound.play()
        
        
    def _apply_pitch_shift(self, pitch_shift: float):
        arr = pg.sndarray.array(self.sound).copy()
        
        # o pitch shift indica semitons de deslocamento. Uma oitava (12 semitons) dobra a frequência do som.
        factor = 2**(pitch_shift/12)
        
        indices = np.round(np.arange(0, len(arr), factor))
        indices = indices[indices < len(arr)].astype(int)
        
        return pg.sndarray.make_sound(arr[indices])
        
    def stop(self):
        self.sound.stop()
        
class MusicAudio:
    def __init__(self, sound_path: str, volume: float = 1):
        pg.mixer.music.load(sound_path)
        pg.mixer.music.set_volume(settings["sounds"]["music_volume"]*volume)
        
    def play(self):
        pg.mixer.music.play(-1)
        
    def stop(self):
        pg.mixer.music.stop()