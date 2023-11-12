import pygame 
from quadrado import Square

square_size = 64

class Level:
	def __init__(self,level_data,surface):
		self.display_surface = surface 
		self.setup_level(level_data)
    
	def setup_level(self,layout):
		self.squares = pygame.sprite.Group()

		for row_index,row in enumerate(layout):
			for col_index,cell in enumerate(row):
				x = col_index * square_size
				y = row_index * square_size
				if cell == 'X':
					square = Square((x,y),square_size)
					self.squares.add(square)
     
	def run(self):
		self.squares.draw(self.display_surface)
