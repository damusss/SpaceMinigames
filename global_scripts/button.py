import pygame
from settings import *

class ButtonGM0():
    def __init__(self,type):

        self.image = pygame.image.load(f'gamemode_0/assets/buttons/{type}_gm_0.png').convert_alpha()
        self.rect = self.image.get_rect(center = (WIDTH//2,HEIGHT//2))
        if type == 'pause':
            self.rect.topright = (WIDTH-20,20)
        elif type == 'exit':
            self.rect.bottomright = (WIDTH-20,HEIGHT-20)

        self.clicked = False

    def draw(self, screen):
        screen.blit(self.image,self.rect)

        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        return action

class ButtonGM1():
    def __init__(self,type):

        self.image = pygame.image.load(f'gamemode_1/assets/buttons/{type}_gm_1.png').convert_alpha()
        self.rect = self.image.get_rect(center = (WIDTH//2,HEIGHT//2-self.image.get_height()))
        if type == 'exit':
            self.rect.centery = HEIGHT//2+self.image.get_height()

        self.clicked = False

    def draw(self, screen):
        screen.blit(self.image,self.rect)

        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        return action

class ButtonGM2():
    def __init__(self,type,font):

        self.color = 'green'
        self.image = font.render('Text',False,'white')
        if type == 'resume':
            self.image = font.render('     RESUME     ',False,'green')
        elif type == 'exit':
            self.image = font.render('       EXIT       ',False,'red')
            self.color = 'red'
        elif type == 'reset':
            self.image = font.render('  TRY AGAIN  ',False,'green')
        elif type == 'win':
            self.image = font.render('  PLAY AGAIN  ',False,'green')
        elif type == 'toggle':
            self.image = font.render(' TOGGLE OLD STYLE ',False,'yellow')
            self.color = 'yellow'
        self.rect = self.image.get_rect(center = (WIDTH//2,HEIGHT//2-self.image.get_height()))
        if type == 'exit':
            self.rect.centery = HEIGHT//2+self.image.get_height()
        elif type == 'toggle':
            self.rect.centery = HEIGHT//2+self.image.get_height()+self.image.get_height()+50

        self.clicked = False

    def draw(self, screen):
        pygame.draw.rect(screen,(30,30,30),self.rect.inflate(15,15))
        pygame.draw.rect(screen,self.color,self.rect.inflate(15,15),3)
        screen.blit(self.image,self.rect)

        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        return action

class ButtonGM3():
    def __init__(self,type,start_color,x,y,scale,font,text_label,is_text,button_text=None,text_color=None):

        if not is_text:
            self.image = pygame.image.load(f'gamemode_3/assets/buttons/{type}.png').convert_alpha()
            self.image = pygame.transform.scale(self.image,(int(self.image.get_width()*scale),int(self.image.get_height()*scale)))
            self.rect = self.image.get_rect(topright=(x,y))
        else:
            self.image = font.render(button_text,False,text_color)
            self.rect = self.image.get_rect(topleft=(x,y))
        self.color = start_color
        self.inflate_x = 15
        if type == 'tank' or type == 'water':
            self.inflate_x = 16

        self.label = font.render(text_label,False,(0,255,255))
        if not is_text:
            self.label_rect = self.label.get_rect(topright=(self.rect.midleft[0]-20,self.rect.midleft[1]-self.label.get_height()//2))
        else:
            self.label_rect = self.label.get_rect(topleft=(self.rect.midright[0]+20,self.rect.midright[1]-self.label.get_height()//2))

        self.clicked = False

    def draw(self, screen,color='blue'):
        pygame.draw.rect(screen,(30,30,30),self.rect.inflate(self.inflate_x,15))
        pygame.draw.rect(screen,color,self.rect.inflate(self.inflate_x,15),3)
        screen.blit(self.image,self.rect)
        screen.blit(self.label,self.label_rect)

        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        return action

class ButtonGM3PauseActions():
    def __init__(self,centerx,centery,type,font,color,text):

        self.image = font.render(text,False,color)
        self.rect = self.image.get_rect(center = (centerx,centery))
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen,(30,30,30),self.rect.inflate(15,15))
        pygame.draw.rect(screen,self.color,self.rect.inflate(15,15),3)
        screen.blit(self.image,self.rect)

        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        return action


class ButtonMainMenu():
    def __init__(self,type):

        self.image = pygame.image.load(f'global_assets/images/arrow_buttons/arrow_{type}.png').convert_alpha()
        self.rect = self.image.get_rect(center = (WIDTH//2,HEIGHT//2))
        if type == 'left':
            self.rect.centerx = 200
        else:
            self.rect.centerx = WIDTH-200

        self.clicked = False

    def draw(self, screen):
        screen.blit(self.image,self.rect)

        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        return action