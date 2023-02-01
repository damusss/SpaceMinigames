import pygame
from math import pi,atan2

class GroundFire(pygame.sprite.Sprite):
    def __init__(self,x,size_width,ground):
        pygame.sprite.Sprite.__init__(self)

        self.size_width = size_width
        self.images = self.import_images()
        self.image = self.images[0]
        self.rect = self.image.get_rect(bottomleft = (x,ground))
        self.frame_index = 0
        self.speed = 0.05

    def animate(self):
        self.frame_index+=self.speed
        if self.frame_index > len(self.images)-1:
            self.frame_index = 0
        self.image = self.images[int(self.frame_index)]

    def import_images(self):
        images = []
        for i in range(3):
            img = pygame.image.load(f'gamemode_3/assets/fire/ground/frame_{i}_delay-0.1s.png').convert_alpha()
            img = pygame.transform.scale(img,(int(self.size_width),int(self.size_width)))
            images.append(img)
        return images

    def update(self):

        self.animate()

class MeteorFire():
    def __init__(self,start_x,start_y,size_width,dir_x,dir_y):
        self.angle = 0
        self.dir_x = dir_x
        self.dir_yy = dir_y
        self.size_width = size_width
        self.img = pygame.image.load(f'gamemode_3/assets/fire/meteor/frame_00_delay-0.1s.png').convert_alpha()
        self.img = pygame.transform.scale(self.img,(int(self.size_width),int(self.size_width*5)))
        self.images = self.import_images()
        self.image = self.orig_image = self.images[0]
        self.rect = self.image.get_rect(center = (start_x,start_y))
        self.frame_index = 0
        self.speed = 0.1

    def draw(self,screen):
        screen.blit(self.image,self.rect)

    def update_pos(self,new_x,new_y):
        self.rect.center = (new_x,new_y+5)
        offset = (self.rect.width-self.img.get_width())//2
        if self.dir_x >= 0:
            self.rect.centerx -= offset
        else:
            self.rect.centerx += offset

    def animate(self):
        self.frame_index+=self.speed
        if self.frame_index > len(self.images)-1:
            self.frame_index = 0
        self.image = self.images[int(self.frame_index)]

    def import_images(self):
        images = []
        for i in range(8):
            img = pygame.image.load(f'gamemode_3/assets/fire/meteor/frame_0{i}_delay-0.1s.png').convert_alpha()
            img = pygame.transform.scale(img,(int(self.size_width),int(self.size_width*3)))
            self.angle = (180 / pi) * -atan2(self.dir_yy, self.dir_x)
            img = pygame.transform.rotate(img, int(self.angle+90))
            images.append(img)
        return images

    def update(self):

        self.animate()