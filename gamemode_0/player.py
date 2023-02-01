import pygame
from math import pi, atan2
from gamemode_0.settings import *
from gamemode_0.points import Laser

class Player():
    def __init__(self,x,y,l_sound):

        self.original_images = self.import_images()
        self.image = self.original_images[0]
        self.rect = self.image.get_rect(center = (x,y))
        self.frame_index = 0
        self.speed = 0.25

        self.x_dir = 0
        self.y_dir = 0

        self.lasers = pygame.sprite.Group()
        self.shooted = False

        self.hitbox = self.rect.inflate(-80,-80)

        self.lives = 3
        self.is_dead = False
        self.laser_s = l_sound

    def import_images(self):
        images = []
        for i in range(3):
            img = pygame.image.load(f'gamemode_0/assets/player/frame_{i}.png').convert_alpha()
            scale = 0.4
            img = pygame.transform.scale(img,(int(img.get_width()*scale),int(img.get_height()*scale))) 
            images.append(img)
        return images

    def input(self):
        mouse1 = pygame.mouse.get_pressed()[0]

        if mouse1:
            if not self.shooted:
                if not self.is_dead:
                    new_laser = Laser(self.rect.centerx,self.rect.centery,LASER_SIZE)
                    self.lasers.add(new_laser)
                    self.shooted = True
                    self.laser_s.play()
        if not mouse1:
            self.shooted = False

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        angle = (180 / pi) * -atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.original_images[int(self.frame_index)], int(angle-90))
        self.rect = self.image.get_rect(center=(self.rect.centerx,self.rect.centery))
        self.x_dir = rel_x // PLAYER_SPEED_DIVIDER
        self.y_dir = rel_y // PLAYER_SPEED_DIVIDER
        if self.x_dir >= 7:
            self.x_dir = 7
        elif self.x_dir <= -7:
            self.x_dir = -7
        if self.y_dir >= 7:
            self.y_dir = 7
        elif self.y_dir <= -7:
            self.y_dir = -7

    def draw(self,screen):
        if not self.is_dead:
            screen.blit(self.image,self.rect)

    def animate(self):
        self.frame_index += self.speed
        if self.frame_index >= 3:
            self.frame_index = 0

    def update(self):

        if not self.is_dead:

            self.animate()

            self.input()

            self.rotate()