import pygame

class Asteroid(pygame.sprite.Sprite):
    def __init__(self,type,pos):
        super().__init__()

        self.image = pygame.image.load(f'gamemode_1/assets/asteroids/{type}.png')
        scale = 2.9
        if type == 6 or type == 7:
            self.image = pygame.transform.scale(self.image,(int(self.image.get_width()*scale),int(self.image.get_height()*scale)))
        self.rect = self.image.get_rect(center = pos)

        self.speed = 15

    def update(self):
        self.rect.x -= self.speed

        if self.rect.right <= 0:
            self.kill()