import pygame
from gamemode_1.settings import HEALTH_COLOR
from gamemode_3.settings import *
from global_scripts.explosion import Explosion

class Tank(pygame.sprite.Sprite):
    def __init__(self,x,y,type,ground):
        pygame.sprite.Sprite.__init__(self)

        self.ground = ground
        self.normal_image = pygame.image.load(f'gamemode_3/assets/tanks/{type}.png').convert_alpha()
        self.normal_image = pygame.transform.scale(self.normal_image,(int(self.normal_image.get_width()*0.5),int(self.normal_image.get_height()*0.5)))
        self.flipped_image = pygame.transform.flip(self.normal_image,True,False)
        self.image = self.normal_image
        self.rect = self.image.get_rect(center = (x,y))
        self.gravity_start = 0.5
        self.gravity = 0

        # timers
        self.last_shoot = 0
        self.shoot_cooldown = 1000
        self.last_damage = 0
        self.damage_cooldown = 1000

        # others
        self.health = 100
        self.max_health = 100
        self.on_ground = False
        self.is_dead = False

        # ui
        self.bar_width = self.image.get_width()
        self.health_bar = pygame.Rect(self.rect.bottomleft[0],self.rect.bottomleft[1],self.max_health,HEALTH_BAR_HEIGHT)
        self.bg_bar = pygame.Rect(self.rect.bottomleft[0],self.rect.bottomleft[1],self.max_health,HEALTH_BAR_HEIGHT)
        self.bg_bar.width = self.health * (self.bar_width/self.max_health)

    def check_death(self):
        if self.health <= 0:
            self.health = 0
            self.is_dead = True

    def change_image(self,meteor_x):
        if meteor_x - self.rect.x >= 0:
            self.image = self.normal_image
        else:
            self.image = self.flipped_image

    def fall(self):
        self.gravity += self.gravity_start
        self.rect.y += self.gravity

    def update(self,screen):
        if self.rect.bottom < self.ground:
            self.fall()
        elif self.rect.bottom > self.ground:
            self.rect.bottom = self.ground
            self.gravity = 0
            self.on_ground = True
        else:
            self.gravity = 0
            self.on_ground = True

        if self.on_ground:
            self.draw_ui(screen)

        self.check_death()

    def draw_ui(self,screen):

        self.health_bar.width = self.health * (self.bar_width / self.max_health)

        self.health_bar.left = self.rect.bottomleft[0]
        self.health_bar.top = self.rect.bottomleft[1]+5
        self.bg_bar.left = self.rect.bottomleft[0]
        self.bg_bar.top = self.rect.bottomleft[1]+5

        pygame.draw.rect(screen,BG_COLOR,self.bg_bar.inflate(3,3))
        pygame.draw.rect(screen,(20,20,20),self.bg_bar.inflate(6,6),3)
        pygame.draw.rect(screen,HEALTH_COLOR,self.health_bar)