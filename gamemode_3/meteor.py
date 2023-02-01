import pygame
from gamemode_3.settings import *
from gamemode_3.fire import MeteorFire

class Meteor(pygame.sprite.Sprite):
    def __init__(self,x,y,type,scale,pos_x,pos_y):
        pygame.sprite.Sprite.__init__(self)

        self.image_o = pygame.image.load(f'gamemode_3/assets/meteors/{type}.png').convert_alpha()
        self.image_o = pygame.transform.scale(self.image_o,(int(self.image_o.get_width()*scale),int(self.image_o.get_height()*scale)))
        self.image = self.image_o
        self.rect = self.image.get_rect(center = (x,y))

        self.dir_x = self.get_direction(pos_x,pos_y)[0]
        self.dir_y = self.get_direction(pos_x,pos_y)[1]

        self.fire = MeteorFire(self.rect.centerx,self.rect.centery,self.image.get_width(),self.dir_x,self.dir_y)

    def get_direction(self,x,y):
        rel_x,rel_y = x -self.rect.centerx,y-self.rect.centery

        dir_x,dir_y = rel_x/A_CONSTANT,rel_y/A_CONSTANT

        return [dir_x,dir_y]

    def move(self):
        self.rect.x += self.dir_x
        self.rect.y += self.dir_y

    def update(self,screen):

        self.move()

        self.fire.draw(screen)

        self.fire.update()

        self.fire.update_pos(self.rect.centerx,self.rect.centery-self.fire.image.get_height()//2)
