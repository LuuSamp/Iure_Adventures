import pygame as pg
from game.const import SCREEN_WIDTH, SCREEN_HEIGHT
from components.slider import Slider
from game.helpers import load_image
from game.settings import Settings
from components.button import Button

class OptionsMenu:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.font = pg.font.Font(None, 32)
        self.text = self.font.render("Options", True, (255, 255, 255))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (SCREEN_WIDTH/2, 100)
        
        self.slider_music = Slider(SCREEN_WIDTH/2, 200, 200, 20, Settings.get_music_volume())
        self.slider_sfx = Slider(SCREEN_WIDTH/2, 300, 200, 20, Settings.get_sfx_volume())
        
        self.scaled_background = load_image("media/background/background_frame.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.back_img = load_image("media/button_images/fast-backward-button.png", None, alpha=True)
        self.back_button = Button( 100, 100, self.back_img, self.back_img, 0.8)
        
    def draw(self):
        self.screen.blit(self.scaled_background, (0, 0))
        self.screen.blit(self.text, self.text_rect)
        self.slider_music.draw(self.screen)
        self.slider_sfx.draw(self.screen)
        if self.back_button.draw_button(self.screen):
            Settings.save_settings()
            return False
        return True
        
    def update(self):
        self.slider_music.update()
        self.slider_sfx.update()
        Settings.set_music_volume(self.slider_music.value)
        Settings.set_sfx_volume(self.slider_sfx.value)
    
    def run(self):
        self.update()
        return self.draw()