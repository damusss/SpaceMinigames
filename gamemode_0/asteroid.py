import pygame
from gamemode_0.settings import *
import time

class Asteroid(pygame.sprite.Sprite):
    def __init__(self,x,y,scale,type,angle,player_x,player_y):
        pygame.sprite.Sprite.__init__(self)

        self.image_o = pygame.image.load(f'gamemode_0/assets/asteroids/{type}.png').convert_alpha()
        self.image_o = pygame.transform.scale(self.image_o,(int(self.image_o.get_width()*scale),int(self.image_o.get_height()*scale)))
        self.image = pygame.transform.rotate(self.image_o,angle)
        self.rect = self.image.get_rect(center = (x,y))

        self.dir_x = self.get_direction(player_x,player_y)[0]
        self.dir_y = self.get_direction(player_x,player_y)[1]

    def get_direction(self,x,y):
        rel_x,rel_y = x -self.rect.centerx,y-self.rect.centery

        dir_x,dir_y = rel_x/A_CONSTANT,rel_y/A_CONSTANT

        return [dir_x,dir_y]

    def move(self):
        self.rect.x += self.dir_x
        self.rect.y += self.dir_y

    def update(self):

        self.move()