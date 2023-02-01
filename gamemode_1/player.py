import pygame
from gamemode_1.settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, ground_y_pos):
        super().__init__()

        scale = 0.17
        image_ufo = pygame.image.load('gamemode_1/assets/player/ufo.png')
        self.image_ufo = pygame.transform.scale(image_ufo,(int(image_ufo.get_width() * scale),int(image_ufo.get_height() * scale)))
        image_walk = pygame.image.load('gamemode_1/assets/player/walk.png')
        self.image_walk = pygame.transform.scale(image_walk,(int(image_walk.get_width() * scale),int(image_walk.get_height() * scale)))
        self.image = self.image_ufo
        self.rect = self.image.get_rect(topleft = (100,HEIGHT//2 - self.image.get_height()//2)).inflate(int(-(self.image.get_width()//3)),int(-(self.image.get_height()//3)))
        self.hitbox = self.rect

        self.global_gravity = 1.6
        self.gravity = self.global_gravity
        self.jump_speed = -27
        self.on_floor = False
        self.is_jumping = False
        self.can_jump = True

        self.ground = ground_y_pos

        self.max_health = 100
        self.max_shield = 100
        self.health = self.max_health
        self.shield = self.max_shield

        self.is_dead = False

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
            if self.can_jump:
                self.jump()
                self.can_jump = False
        else: 
            self.can_jump = True
            self.is_jumping = False

    def jump(self):
        self.is_jumping = True
        self.on_floor = False
        self.gravity = self.jump_speed

    def fall(self):
        if not self.on_floor:
            self.gravity += self.global_gravity
            self.rect.y += self.gravity

    def world_collisions(self):
        if self.rect.top < 0:
            self.rect.top = 0
            self.on_floor = False
        elif self.rect.bottom >= self.ground + 40:
            self.image = self.image_walk
            self.rect.bottom = self.ground +40
            if not self.is_jumping:
                self.on_floor = True
        else:
            self.on_floor = False

        if self.rect.bottom < self.ground:
            self.image = self.image_ufo

    def update(self):
        
        self.fall()

        self.world_collisions()

        self.input()