import pygame as pg

class Slider:
    def __init__(self, x: int, y: int, width: int, height: int, value: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.value = value
        self.dragging = False
        
        self.rect = pg.Rect(self.x-self.width/2, self.y+self.height/2, self.width, self.height)
        
    def draw(self, surface: pg.Surface):
        pg.draw.rect(surface, (255, 255, 255), self.rect)
        pg.draw.rect(surface, (0, 0, 0), (self.x-self.width/2, self.y+self.height/2, self.width * self.value, self.height))
        
    def update(self):
        self.handle_events()
        
    def handle_events(self):
        mouse_pos = pg.mouse.get_pos()
        
        if (self.rect.collidepoint(mouse_pos)):
            if pg.mouse.get_pressed()[0] == 1:
                self.dragging = True
            else:
                self.dragging = False
                
            self.handle_mouse_motion(mouse_pos)
                
    def handle_mouse_motion(self, pos: tuple[int, int]):
        if self.dragging:
            self.value = (pos[0] - self.x) / self.width
            self.value = max(0, min(self.value, 1))
            
        return self.value