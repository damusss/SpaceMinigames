import pygame
from random import choice,randint,uniform
from gamemode_0.points import Star
from gamemode_0.player import Player
from gamemode_0.asteroid import Asteroid
from global_scripts.explosion import Explosion
from global_scripts.button import ButtonGM0
from gamemode_0.settings import *

class LevelGM0():
    def __init__(self,screen,quit):

        self.click_sound = pygame.mixer.Sound('global_assets/audio/select.wav')
        self.click_sound.set_volume(0.15)
        
        self.screen = screen
        self.score_font = pygame.font.Font('global_assets/font/font_pixel.ttf',40)
        self.game_paused = False
        self.pause_type = 'none'
        self.can_pause = True
        self.restart_button = ButtonGM0('restart')
        self.pause_button = ButtonGM0('pause')
        self.exit_button = ButtonGM0('exit')

        # player
        self.laser_sound = pygame.mixer.Sound('global_assets/audio/laser.wav')
        self.laser_sound.set_volume(0.06)
        self.player = Player(WIDTH//2,HEIGHT//2,self.laser_sound)

        # groups
        self.star_group = pygame.sprite.Group()
        self.asteroid_group = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        # startup
        self.create_stars()

        # cooldown
        self.ast_cooldowns = [1000,3000]
        self.last_ast = 0

        # gui
        self.score = 0
        scale = 0.05
        self.heart_img = pygame.image.load('gamemode_0/assets/gui/hearth.png').convert_alpha()
        self.heart_img = pygame.transform.scale(self.heart_img,(int(self.heart_img.get_width()*scale),int(self.heart_img.get_height()*scale)))
        self.score_img = self.score_font.render('Score: ',False,'white')
        self.score_rect = self.score_img.get_rect(center = (WIDTH//2,20))
        self.kills = 0
        self.kills_img = self.score_font.render('Kills: '+str(self.kills),False,'white')
        self.kills_rect = self.kills_img.get_rect(center = (WIDTH//2,HEIGHT-50))

        self.quit = quit

        self.music = pygame.mixer.Sound('global_assets/audio/music/music_gm_0.wav')
        self.music_volume = 0.5
        self.music.set_volume(self.music_volume)

        self.exp_sound = pygame.mixer.Sound('global_assets/audio/explosion_strong.wav')
        self.exp_sound_smol = pygame.mixer.Sound('global_assets/audio/explosion_small.wav')
        self.exp_sound.set_volume(0.12)
        self.exp_sound_smol.set_volume(0.2)

    def create_stars(self):
        while len(self.star_group) < STARS_NUM:
            random_x = randint(0,WIDTH)
            random_y = randint(0,HEIGHT)
            random_size = choice(STAR_SIZES)
            new_star = Star(random_x,random_y,random_size)
            self.star_group.add(new_star)

    def asteroids_collisions(self):
        if self.asteroid_group:
            for a in self.asteroid_group:
                if pygame.Rect.colliderect(a.rect,self.player.hitbox):
                    a.kill()
                    self.exp_sound.play()
                    expl = Explosion(a.rect.centerx,a.rect.centery,a.image.get_width())
                    self.explosions.add(expl)
                    self.player.lives -= 1
                    if self.player.lives <= 0:
                        self.exp_sound.play()
                        self.game_paused = True
                        self.pause_type = 'dead'
                        self.player.lives = 0
                        self.player.is_dead = True
                        expl_n = Explosion(self.player.rect.centerx,self.player.rect.centery,self.player.image.get_width()+30)
                        self.explosions.add(expl_n)
                if self.player.lasers:
                    for l in self.player.lasers:
                        if pygame.Rect.colliderect(a.rect,l.rect):
                            self.score += randint(5,10)
                            l.kill()
                            a.kill()
                            expl = Explosion(a.rect.centerx,a.rect.centery,a.image.get_width())
                            self.explosions.add(expl)
                            self.exp_sound_smol.play()
                            self.kills += 1

    def spawn_asteroids(self):
        if pygame.time.get_ticks() - self.last_ast > randint(self.ast_cooldowns[0],self.ast_cooldowns[1]):
            rand_type = randint(0,A_TYPE_NUMS)
            rand_scale = uniform(1.01,2.01)
            rand_angle = randint(0,260)
            r_dir = choice(A_DIR)
            r_x = r_y = 0
            if r_dir == 'up' or r_dir == 'down':
                r_x = randint(0,WIDTH)
                if r_dir == 'up':
                    r_y = -50
                elif r_dir == 'down':
                    r_y == HEIGHT+50
            else:
                r_y = randint(0,HEIGHT)
                if r_dir == 'left':
                    r_x = -50
                elif r_dir == 'right':
                    r_x = WIDTH+50
            new_ast = Asteroid(r_x,r_y,rand_scale,rand_type,rand_angle,self.player.rect.centerx,self.player.rect.centery)
            self.asteroid_group.add(new_ast)
            self.last_ast = pygame.time.get_ticks()

    def pause_actions(self):
        if self.pause_type == 'dead':
            if self.restart_button.draw(self.screen):
                self.asteroid_group.empty()
                self.player.lasers.empty()
                self.player.lives = 3
                self.player.is_dead = False
                self.pause_type = 'none'
                self.score = 0
                self.game_paused = False
                self.click_sound.play()
            if self.exit_button.draw(self.screen):
                self.quit()
                self.click_sound.play()
        elif self.pause_type == 'key':
            if self.pause_button.draw(self.screen):
                self.pause_type = 'none'
                self.game_paused = False
                self.click_sound.play()
            if self.exit_button.draw(self.screen):
                self.quit()
                self.click_sound.play()

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            if self.can_pause:
                if not self.game_paused:
                    self.game_paused = True
                    self.pause_type = 'key'
                elif self.game_paused and self.pause_type != 'dead':
                    self.game_paused = False
                    self.pause_type = 'key'
                    self.click_sound.play()
                self.can_pause = False
        elif not keys[pygame.K_ESCAPE]:
            self.can_pause = True

    def update_score(self):
        self.score_img = self.score_font.render('Score: '+str(self.score),False,'white')
        self.score_rect = self.score_img.get_rect(center = (WIDTH//2,50))
        self.kills_img = self.score_font.render('Kills: '+str(self.kills),False,'white')
        self.kills_rect = self.kills_img.get_rect(center = (WIDTH//2,HEIGHT-50))

    def draw_ui(self):
        if self.player.lives > 0:
            for i in range(self.player.lives):
                self.screen.blit(self.heart_img,(20+self.heart_img.get_width()*i,20))

        pygame.draw.rect(self.screen,(30,30,30),self.score_rect.inflate(15,15))
        pygame.draw.rect(self.screen,(20,20,20),self.score_rect.inflate(15,15),3)
        self.screen.blit(self.score_img,self.score_rect)
        pygame.draw.rect(self.screen,(30,30,30),self.kills_rect.inflate(15,15))
        pygame.draw.rect(self.screen,(20,20,20),self.kills_rect.inflate(15,15),3)
        self.screen.blit(self.kills_img,self.kills_rect)

    def run(self):
        # bg
        self.screen.fill('black')
        self.star_group.update(self.screen)

        # input
        self.input()

        if not self.game_paused:
            pygame.mixer.unpause()
            # checks
            self.asteroids_collisions()
            self.spawn_asteroids()

            # update
            self.player.update()
            self.asteroid_group.update()
            self.update_score()

        # draw
        self.player.lasers.update(self.screen,self.game_paused)
        self.player.draw(self.screen)
        self.asteroid_group.draw(self.screen)
        self.explosions.update()
        self.explosions.draw(self.screen)
        self.draw_ui()

        if self.game_paused:
            pygame.mixer.pause()
            self.pause_actions()

    def destroy(self):
        self.score = 0
        self.player.lives = 3
        self.game_paused = False
        self.pause_type = 'none'
        self.asteroid_group.empty()
        self.player.lasers.empty()
        self.explosions.empty()
        self.kills = 0