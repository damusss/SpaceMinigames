import pygame
from gamemode_3.settings import *

class Planet(pygame.sprite.Sprite):
    def __init__(self,type,scale,x,y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(f'gamemode_3/assets/planets/{type}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(int(self.image.get_width()*scale),int(self.image.get_height()*scale)))

        self.rect = self.image.get_rect(center = (x,y))