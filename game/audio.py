import pygame as pg
import json
from os import path
import random
import numpy as np
from game.settings import Settings
from abc import abstractmethod, ABC
    
class SFXAudio:
    def __init__(self, sound_path: str, volume: float = 1, pitch_shift_sigma: float = 1, pitch_shift_cap: float = 1.5):
        self.pitch_shift_sigma = pitch_shift_sigma
        self.pitch_shift_cap = pitch_shift_cap
        self.sound = pg.mixer.Sound(sound_path)
        self.volume = volume
        
    def play(self):
        
        if self.pitch_shift_sigma == 0: 
            self.sound.set_volume(self._true_volume())
            self.sound.play()
            return
        
        shift = random.gauss(0, self.pitch_shift_sigma)
        if abs(shift) > self.pitch_shift_cap:
            shift = self.pitch_shift_cap * np.sign(shift)
        
        new_sound = self._apply_pitch_shift(shift)
        new_sound.set_volume(self._true_volume())
        new_sound.play()
        
    def _true_volume(self):
        return Settings.get_sfx_volume()*self.volume
        
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
        self.volume = volume
        pg.mixer.music.load(sound_path)
        pg.mixer.music.set_volume(self._true_volume())
        
    def play(self):
        pg.mixer.music.play(-1)
        
    def update(self):
        pg.mixer.music.set_volume(self._true_volume())
    
    def _true_volume(self):
        return Settings.get_music_volume()*self.volume
        
    def stop(self):
        pg.mixer.music.stop()