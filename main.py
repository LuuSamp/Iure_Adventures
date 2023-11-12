import pygame, sys
from geral import Level

map_test = [
'                            ',
'                            ',
'                            ',
'                      XX    ',
'                            ',
'                         XX ',
'                            ',
' XX    X  XXXX              ',
'      XX  XXXX        XXX   ',
'XXXXXXXX  XXXXXX  XX  XXXX  ',
'XXXXXXXX  XXXXXX  XX  XXXX  ']

square_size = 64
screen_width = 1200
screen_height = len(map_test) * square_size

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
level = Level(map_test,screen)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	
	screen.fill('black')
	level.run()

	pygame.display.update()
	clock.tick(60)