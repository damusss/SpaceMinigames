import pygame
from settings import *

class SpaceStation():
    def __init__(self,ground):

        scale = 0.25
        self.image = pygame.image.load('gamemode_3/assets/space_station/space_station.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(int(self.image.get_width()*scale),int(self.image.get_height()*scale)))
        self.rect = self.image.get_rect(bottomleft = (WIDTH//2-self.image.get_width()//2,ground))
        self.hitbox_1 = self.rect.inflate(-170,-150)
        self.hitbox_1.x+= 57
        self.hitbox_2 = self.hitbox_1.inflate(-200,0)
        self.hitbox_2.x -= 220
        self.hitbox_2.y += 75
        self.max_health = 5000
        self.health = 5000
        self.last_damage = 0
        self.damage_cooldown = 500

    def draw(self,screen):
        screen.blit(self.image,self.rect)