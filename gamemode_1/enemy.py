import pygame
from settings import WIDTH
from gamemode_1.laser import Laser

class Enemy(pygame.sprite.Sprite):
    def __init__(self,type,pos):
        super().__init__()
        
        self.image = pygame.image.load(f'gamemode_1/assets/spaceships/{type}.png')
        self.rect = self.image.get_rect(topleft = pos)

    def update(self):
        if self.rect.right > WIDTH - 20:
            self.rect.x -= 10