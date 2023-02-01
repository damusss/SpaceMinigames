# modules
import pygame,sys
# components
from main_menu import MainMenu
# settings
from settings import *

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Minigames")
clock = pygame.time.Clock()
 
class Game():
    def __init__(self):
        
        self.main_menu = MainMenu(screen)

    def run(self):
        
        self.main_menu.run()

game = Game()
 
while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    # game run
    game.run()

    # display update
    clock.tick(FPS)
    pygame.display.update()