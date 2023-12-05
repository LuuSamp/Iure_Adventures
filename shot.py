import pygame as pg

class Shot(pg.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        
        self.sound = pg.mixer.Sound("media\shooting-sound-fx-159024.mp3")
        self.sound.play()

        self.x_vel = 6
        self.image = pg.image.load("media\B1.png")
        self.image = pg.transform.scale(self.image, (25, 7))
        self.rect = self.image.get_rect(topleft = position)
        self.initial_pos = self.rect.left
        self.direction = -1

        self.current_frame = 0
        self.animation_frames = [
            pg.image.load("media\B1.png"),
            pg.image.load("media\B2.png")                                                 
        ]
        self.animation_counter = 0
        self.animation_delay = 15

    def animation(self):
        if self.animation_counter >= self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            frame = pg.transform.scale(self.animation_frames[self.current_frame], (self.rect.width, self.rect.height))
            self.image = frame
            self.animation_counter = 0

        self.animation_counter += 1
        

    def update(self):
        self.rect.left += self.direction * self.x_vel
        if self.initial_pos - self.rect.left > 300:
            self.kill()
        self.animation()