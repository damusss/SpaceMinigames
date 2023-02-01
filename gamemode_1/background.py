import pygame
from gamemode_1.settings import *

class BG:
    def __init__(self):
        bg_scale = 1.463
        self.bg = pygame.image.load('gamemode_1/assets/bg/space.png')
        self.bg = pygame.transform.scale(self.bg,(int(WIDTH),int(HEIGHT)))
        self.bg_rect = self.bg.get_rect(topleft = (0,0))
        self.bg_speed = 2
        self.ground_img = pygame.image.load('gamemode_1/assets/bg/ground.png')
        g_x = 0
        g_y = HEIGHT-150
        ground_scale = 0.3
        self.ground_img = pygame.transform.scale(self.ground_img,(int(self.ground_img.get_width() * ground_scale),int(self.ground_img.get_height() * ground_scale)))
        self.ground_rect = self.ground_img.get_rect(topleft = (g_x,g_y))
        self.ground_offset = self.ground_img.get_width()
        self.ground_dir_y = 1
        self.ground_step = 40
        self.ground_stepped = 0

    def draw_bg(self,screen,pause):
        screen.blit(self.bg,self.bg_rect)
        screen.blit(self.bg,(self.bg_rect.x+self.bg.get_width(),self.bg_rect.y+0))

        if not pause: self.bg_rect.x -= self.bg_speed

        if self.bg_rect.right <= 0:
            self.bg_rect.left = 0

        self.draw_ground(screen,pause)

    def draw_ground(self,screen,pause):
        
        screen.blit(self.ground_img,(self.ground_rect.x ,self.ground_rect.y))

        if not pause: 
            self.ground_rect.y += 1*self.ground_dir_y

            self.ground_stepped += 1
            if self.ground_stepped >= self.ground_step:
                self.ground_dir_y *= -1
                self.ground_stepped = 0