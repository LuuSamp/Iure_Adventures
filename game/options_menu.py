import pygame as pg
from game.const import SCREEN_WIDTH, SCREEN_HEIGHT
from components.slider import Slider
from game.helpers import load_image
from game.settings import Settings
from components.button import Button

_FONT = "media/button_images/PressStart2P-Regular.ttf"


class OptionsMenu:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.scaled_background = load_image(
            "media/background/background_frame.png", (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        cx = SCREEN_WIDTH // 2
        slider_w, slider_h = 360, 18

        self.title_font = pg.font.Font(_FONT, 40)
        self.label_font = pg.font.Font(_FONT, 18)

        self.title = self.title_font.render("OPTIONS", True, "white")
        self.title_rect = self.title.get_rect(center=(cx, 140))

        self.music_label = self.label_font.render("Music", True, "white")
        self.music_label_rect = self.music_label.get_rect(center=(cx, 250))
        self.slider_music = Slider(cx, 270, slider_w, slider_h, Settings.get_music_volume())

        self.sfx_label = self.label_font.render("SFX", True, "white")
        self.sfx_label_rect = self.sfx_label.get_rect(center=(cx, 360))
        self.slider_sfx = Slider(cx, 380, slider_w, slider_h, Settings.get_sfx_volume())

        self.back_img = load_image("media/button_images/fast-backward-button.png", None, alpha=True)
        self.back_button = Button(80, 80, self.back_img, self.back_img, 0.7)

    def draw(self):
        self.screen.blit(self.scaled_background, (0, 0))
        self.screen.blit(self.title, self.title_rect)
        self.screen.blit(self.music_label, self.music_label_rect)
        self.screen.blit(self.sfx_label, self.sfx_label_rect)
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
