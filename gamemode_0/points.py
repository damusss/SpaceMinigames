import pygame
from gamemode_0.settings import *

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

class Laser(pygame.sprite.Sprite):
    def __init__(self,x,y,size):
        pygame.sprite.Sprite.__init__(self)

        self.size = size
        self.image = pygame.Surface((self.size,self.size))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(center = (x,y))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        self.x_dir = rel_x // L_SPEED_DIVIDER
        self.y_dir = rel_y // L_SPEED_DIVIDER

    def check_kill(self):
        if self.rect.x > 0-10 and self.rect.x < WIDTH+10 and self.rect.y > 0-10 and self.rect.y < HEIGHT+10:
            pass
        else:
            self.kill()

    def custom_draw(self,screen):
        
        pygame.draw.circle(screen,LASER_COLOR,(self.rect.centerx,self.rect.centery),self.size/2,self.size)

    def move(self):
        self.rect.x += self.x_dir
        self.rect.y += self.y_dir

    def update(self,screen,pause):
        
        self.custom_draw(screen)
        if not pause:
            self.check_kill()

            self.move()