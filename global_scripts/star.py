import pygame
from settings import *

class Star(pygame.sprite.Sprite):
    def __init__(self,x,y,size):
        pygame.sprite.Sprite.__init__(self)

        self.size = size
        self.image = pygame.Surface((self.size,self.size))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(center = (x,y))

    def custom_draw(self,screen):

        pygame.draw.circle(screen,STAR_COLOR,(self.rect.centerx,self.rect.centery),self.size/2,self.size)

    def update(self,screen):
        
        self.custom_draw(screen)