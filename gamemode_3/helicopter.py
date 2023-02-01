import pygame
from gamemode_3.settings import *
from gamemode_1.settings import HEALTH_COLOR

class Helicopter(pygame.sprite.Sprite):
    def __init__(self,x,y,type):
        pygame.sprite.Sprite.__init__(self)

        self.type = type
        self.normal_images = self.import_images('normal')
        self.flipped_images = self.import_images('flipped')
        self.image = self.normal_images[0]
        self.rect = self.image.get_rect(center=(x,y))
        self.frame_index = 0
        self.speed = 0.15
        self.direction = 'normal'

        # timers
        self.last_shoot = 0
        self.shoot_cooldown = 1000

        # others
        self.health = 250
        self.max_health = 250
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
            self.direction = 'flipped'
        else:
            self.direction = 'normal'

    def import_images(self,direction):
        images = []
        for i in range(HELIC_FRAMES):
            img = pygame.image.load(f'gamemode_3/assets/helicopters/{self.type}/frame_{i}_delay-0.1s.png').convert_alpha()
            if direction == 'flipped':
                img = pygame.transform.flip(img,True,False)
            img = pygame.transform.scale(img,(int(img.get_width()*HELIC_SCALE),int(img.get_height()*HELIC_SCALE)))
            images.append(img)
        return images

    def draw_ui(self,screen):

        self.health_bar.width = self.health * (self.bar_width / self.max_health)

        self.health_bar.left = self.rect.bottomleft[0]
        self.health_bar.top = self.rect.bottomleft[1]+5
        self.bg_bar.left = self.rect.bottomleft[0]
        self.bg_bar.top = self.rect.bottomleft[1]+5

        pygame.draw.rect(screen,BG_COLOR,self.bg_bar.inflate(3,3))
        pygame.draw.rect(screen,(20,20,20),self.bg_bar.inflate(6,6),3)
        pygame.draw.rect(screen,HEALTH_COLOR,self.health_bar)

    def animate(self):
        self.frame_index += self.speed
        if self.frame_index >= HELIC_FRAMES:
            self.frame_index = 0
        if self.direction == 'normal':
            self.image = self.normal_images[int(self.frame_index)]
        else:
            self.image = self.flipped_images[int(self.frame_index)]

    def update(self,screen):
        
        self.animate()
        
        self.draw_ui(screen)

        self.check_death()