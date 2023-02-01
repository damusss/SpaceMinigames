import pygame
from gamemode_1.settings import *

class UI:
    def __init__(self,max_h,max_s,score):

        self.bg_health = pygame.Rect(15,15,HEALTH_LENGTH,HEALTH_HEIGHT)
        self.bg_shield = pygame.Rect(15,50,SHIELD_LENGTH,SHIELD_HEIGHT)

        self.health = pygame.Rect(15,15,max_h,HEALTH_HEIGHT)
        self.shield = pygame.Rect(15,50,max_s,SHIELD_HEIGHT)

        self.font = pygame.font.Font('global_assets/font/font_pixel.ttf',30)

        self.surface = pygame.display.get_surface()

    def update_bars(self,h,s,mh,ms):
        self.health.width = h * (HEALTH_LENGTH / mh)
        self.shield.width = s * (SHIELD_LENGTH / ms)

    def show_score(self,score,kills):
        score_surf = self.font.render('Score: '+str(score),False,'white')
        score_rect = score_surf.get_rect(center = (WIDTH//2,40))
        self.surface.blit(score_surf,score_rect)
        kill_surf = self.font.render('Kills: '+str(kills),False,'white')
        kill_rect = kill_surf.get_rect(center = (WIDTH//2,40+score_surf.get_height()))
        self.surface.blit(kill_surf,kill_rect)

    def draw(self,screen,h,s,mh,ms,score,kills):

        self.update_bars(h,s,mh,ms)

        self.show_score(score,kills)

        pygame.draw.rect(screen,BG_COLOR,self.bg_health)
        pygame.draw.rect(screen,BG_COLOR,self.bg_shield)
        pygame.draw.rect(screen,'black',self.bg_health.inflate(5,5),3)
        pygame.draw.rect(screen,'black',self.bg_shield.inflate(5,5),3)
        pygame.draw.rect(screen,HEALTH_COLOR,self.health)
        pygame.draw.rect(screen,SHIELD_COLOR,self.shield)