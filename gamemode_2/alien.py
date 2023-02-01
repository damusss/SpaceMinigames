import pygame 
from random import randint

class Alien(pygame.sprite.Sprite):
    def __init__(self, color,x,y):
        super().__init__()

        file_path = 'gamemode_2/assets/'+color+'.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x,y))
        self.value = 0
        if color == 'red': self.value = randint(3,8)
        elif color == 'green' : self.value = randint(15,25)
        else: self.value = randint(50,60)

    def update(self,direction):
        self.rect.x += direction

class Extra(pygame.sprite.Sprite):
    def __init__(self,side, screen_width):
        super().__init__()

        self.image = pygame.image.load('gamemode_2/assets/extra.png').convert_alpha()
        if side == 'right':
            x = screen_width + 50
            self.speed = -5
        else:
            x = -50
            self.speed = 5
        self.rect = self.image.get_rect(topleft = (x,50))

    def update(self):
        self.rect.x += self.speed
