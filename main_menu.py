import pygame, sys
from random import randint,choice
from settings import *
from global_scripts.star import Star
from global_scripts.button import ButtonMainMenu
from global_scripts.cursor import CustomCursor
from gamemode_0.level import LevelGM0
from gamemode_1.level import LevelGM1
from gamemode_2.level import LevelGM2
from gamemode_3.level import LevelGM3

class MainMenu():
    def __init__(self,screen):
        pygame.mouse.set_visible(False)

        self.click_sound = pygame.mixer.Sound('global_assets/audio/select.wav')
        self.click_sound.set_volume(0.15)

        self.screen = screen
        self.font = pygame.font.Font('global_assets/font/font_pixel.ttf',50)

        # buttons
        self.left_button = ButtonMainMenu('left')
        self.right_button = ButtonMainMenu('right')

        # gamemodes
        self.gamemode_0 = LevelGM0(self.screen,self.quit_game)
        self.gamemode_1 = LevelGM1(self.screen,self.quit_game)
        self.gamemode_2 = LevelGM2(self.screen,self.quit_game)
        self.gamemode_3 = LevelGM3(self.screen,self.quit_game)

        # gamemode
        self.gamemodes_num = 4
        self.gamemode_index = 0
        self.gamemodes = [self.gamemode_0,self.gamemode_1,self.gamemode_2,self.gamemode_3]
        self.gamemode = self.gamemodes[0]
        self.in_game = False
        self.gamemode_images = self.import_images()
        self.gamemode_image = self.gamemode_images[self.gamemode_index]
        w = self.gamemode_image.get_width()
        h = self.gamemode_image.get_height()
        self.gamemode_image = pygame.transform.scale(self.gamemode_image,(int(w*G_SCALES[self.gamemode_index][0]),int(h*G_SCALES[self.gamemode_index][1])))
        self.gamemode_rect = self.gamemode_image.get_rect(center = (WIDTH//2,HEIGHT//2))
        self.gamemode_text = self.font.render(f'Gamemode: {G_NAMES[self.gamemode_index]}',False,'white')
        self.gamemode_txt_rect = self.gamemode_text.get_rect(center = (WIDTH//2,100))
        self.can_change = True

        # high scores
        self.high_scores = self.import_high_scores()
        self.high_score_txt = self.font.render(f'High score: {self.high_scores[self.gamemode_index]}',False,'white')
        self.high_score_txt_rect = self.high_score_txt.get_rect(center = (WIDTH//2,HEIGHT-100))

        # groups
        self.star_group = pygame.sprite.Group()

        # startup
        self.create_stars()

        self.music = pygame.mixer.Sound('global_assets/audio/music/music_main_menu.wav')
        self.music.set_volume(0.5)
        self.music_volume = 0.5

        self.channel_music = pygame.mixer.Channel(0)
        self.channel_music.play(self.music,loops=-1)

        # cursor
        self.cursor = CustomCursor(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

    def import_high_scores(self):
        h_s_list = []
        for i in range(0,self.gamemodes_num):
            with open(f'global_assets/junk/cache/gamemode_{i}.txt','r') as file:
                high_score = int(file.readline())
                h_s_list.append(high_score)
        return h_s_list

    def import_images(self):
        images = []
        for i in range(self.gamemodes_num):
            image = pygame.image.load(f'global_assets/images/gamemodes_icons/{i}.png').convert_alpha()
            images.append(image)
        return images

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.can_change:
                self.change_gamemode('left')
                self.can_change = False
                self.click_sound.play()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.can_change:
                self.change_gamemode('right')
                self.can_change = False
                self.click_sound.play()
        elif keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        
        elif keys[pygame.K_RETURN]:
            self.start_game()
            self.click_sound.play()

        if not any(keys):
            self.can_change = True

    def set_new_high_score(self,new_score):
        with open(f'global_assets/junk/cache/gamemode_{self.gamemode_index}.txt','w') as file:
            file.write(str(new_score))

    def quit_game(self):
        self.in_game = False
        if self.gamemode.score > self.high_scores[self.gamemode_index]:
            self.set_new_high_score(self.gamemode.score)
            self.high_scores = self.import_high_scores()
        self.change_gamemode('quit')
        self.channel_music.play(self.music,loops=-1)

    def change_gamemode(self,dir):
        if dir == 'left':
            if self.gamemode_index > 0:
                self.gamemode_index -= 1
        elif dir == 'right':
            if self.gamemode_index < len(self.gamemodes)-1:
                self.gamemode_index += 1
        self.gamemode_image = self.gamemode_images[self.gamemode_index]
        w = self.gamemode_image.get_width()
        h = self.gamemode_image.get_height()
        self.gamemode_image = pygame.transform.scale(self.gamemode_image,(int(w*G_SCALES[self.gamemode_index][0]),int(h*G_SCALES[self.gamemode_index][1])))
        self.gamemode_rect = self.gamemode_image.get_rect(center = (WIDTH//2,HEIGHT//2))
        self.gamemode_text = self.font.render(f'Gamemode: {G_NAMES[self.gamemode_index]}',False,'white')
        self.gamemode_txt_rect = self.gamemode_text.get_rect(center = (WIDTH//2,100))
        self.high_score_txt = self.font.render(f'High score: {self.high_scores[self.gamemode_index]}',False,'white')
        self.high_score_txt_rect = self.high_score_txt.get_rect(center = (WIDTH//2,HEIGHT-100))

    def start_game(self):
        self.gamemode.destroy()
        self.gamemode = self.gamemodes[self.gamemode_index]
        if self.gamemode_index == 2:
            if self.gamemode.first_time == True:
                self.gamemode.recreate()
        elif self.gamemode_index == 3:
            if self.gamemode.first_time:
                self.gamemode.create_planets()
                if self.gamemode_index == 3:
                    self.gamemode.create_stars()
        self.channel_music.play(self.gamemode.music,loops=-1)
        self.in_game = True

    def arrow_buttons(self):
        if not self.in_game:
            if self.left_button.draw(self.screen):
                self.change_gamemode('left')
                self.click_sound.play()
            if self.right_button.draw(self.screen):
                self.change_gamemode('right')
                self.click_sound.play()

    def draw_text(self):
        pygame.draw.rect(self.screen,(30,30,30),self.gamemode_txt_rect.inflate(15,15))
        pygame.draw.rect(self.screen,(20,20,20),self.gamemode_txt_rect.inflate(15,15),3)
        self.screen.blit(self.gamemode_text,self.gamemode_txt_rect)

        pygame.draw.rect(self.screen,(30,30,30),self.high_score_txt_rect.inflate(15,15))
        pygame.draw.rect(self.screen,(20,20,20),self.high_score_txt_rect.inflate(15,15),3)
        self.screen.blit(self.high_score_txt,self.high_score_txt_rect)

    def create_stars(self):
        while len(self.star_group) < STARS_NUM:
            random_x = randint(0,WIDTH)
            random_y = randint(0,HEIGHT)
            random_size = choice(STAR_SIZES)
            new_star = Star(random_x,random_y,random_size)
            self.star_group.add(new_star)

    def run(self):
        # bg
        self.screen.fill('black')

        #input
        if not self.in_game:
            self.star_group.update(self.screen)
            self.draw_text()
            self.input()
            self.arrow_buttons()
            self.screen.blit(self.gamemode_image,self.gamemode_rect)

        # game
        if self.in_game == True:
            self.gamemode.run()

        # cursor
        pos = pygame.mouse.get_pos()
        self.cursor.update_draw(self.screen,pos[0]+10,pos[1]+10)