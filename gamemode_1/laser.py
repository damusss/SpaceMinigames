import pygame
from gamemode_1.settings import WIDTH

class Laser(pygame.sprite.Sprite):
    def __init__(self,pos,direction,type):
        super().__init__()

        self.image = pygame.image.load(f'gamemode_1/assets/{type}/bullet.png')
        self.rect = self.image.get_rect(topleft = pos)

        self.speed = 0
        if type == 'player':
            self.speed = 25
        else:
            self.speed = 20
        self.direction = direction
        self.type = type

    def destroy(self):
        if self.type == 'player':
            if self.rect.left >= WIDTH:
                self.kill()
        else:
            if self.rect.right <= 0:
                self.kill()

    def update(self):
        self.rect.x += self.speed * self.direction

        self.destroy()