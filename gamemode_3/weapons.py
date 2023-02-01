from tabnanny import check
import pygame
from settings import HEIGHT, WIDTH
from math import radians,sin,cos

class TankBall(pygame.sprite.Sprite):
    def __init__(self,start_x,start_y,angle,who):
        pygame.sprite.Sprite.__init__(self)

        self.start_x,self.start_y = start_x,start_y
        self.image = pygame.image.load('gamemode_3/assets/weapons/ball.png').convert_alpha()
        scale = 0.2
        self.image = pygame.transform.scale(self.image,(int(self.image.get_width()*scale),int(self.image.get_height()*scale)))
        self.rect = self.image.get_rect(center = (start_x+50,start_y))
        self.angle = radians(angle)
        self.speed = 20
        # delta pos
        self.dx = cos(self.angle) * self.speed
        self.dy = -(sin(self.angle) * self.speed)
        self.hitbox = self.rect.copy()
        if who == 'tank':
            self.hitbox = self.rect.inflate(50,50)
        else:
            self.hitbox = self.rect.inflate(15,15)

    def update(self):
        self.hitbox.center = self.rect.center

        # check
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

        # move bullet
        self.rect.x += self.dx
        self.rect.y += self.dy