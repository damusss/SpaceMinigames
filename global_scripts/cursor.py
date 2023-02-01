import pygame

class CustomCursor():
    def __init__(self,startx,starty):

        scale = 0.1
        self.image = pygame.image.load('global_assets/images/cursor.png').convert_alpha()
        #self.image = pygame.transform.scale(self.image,(int(self.image.get_width()*scale),int(self.image.get_height()*scale)))

        self.rect = self.image.get_rect(center=(startx,starty))

    def update_draw(self,screen,x,y):
        self.rect.center = (x,y)

        screen.blit(self.image,self.rect)