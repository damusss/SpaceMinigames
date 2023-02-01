import pygame

class Text():
    def __init__(self,text,start_value,x,y):
        
        self.x = x
        self.y = y
        self.font = pygame.font.Font('global_assets/font/font_pixel.ttf',22)
        self.text_surf = self.font.render(text+str(start_value),False,'white')
        self.text_rect = self.text_surf.get_rect(topleft = (x,y))
        self.text = text

    def draw_text(self,screen,new_value,color='white'):

        pygame.draw.rect(screen,(30,30,30),self.text_rect.inflate(10,10))
        pygame.draw.rect(screen,(20,20,20),self.text_rect.inflate(10,10),3)
        screen.blit(self.text_surf,self.text_rect)

        self.text_surf = self.font.render(self.text+str(new_value),False,color)
        self.text_rect = self.text_surf.get_rect(topleft = (self.x,self.y))

class Message(pygame.sprite.Sprite):
    def __init__(self,x,y,text,color,cooldown):
        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.Font('global_assets/font/font_pixel.ttf',15)
        self.image = self.font.render(text,False,color)
        self.rect = self.image.get_rect(topleft=(x,y))
        self.x = x
        self.y = y
        self.cooldown = cooldown
        self.alpha = 255
        self.finished = False

    def draw_message(self,screen,new_y):

        self.rect.top = self.y + new_y
        screen.blit(self.image,self.rect)

    def fade(self):
        self.alpha -= 1
        if self.alpha <= 0:
            self.alpha = 0
            self.kill()
        self.image.set_alpha(self.alpha)

    def update(self):
        self.cooldown -= 5
        if self.cooldown <= 0:
            self.fade()