import pygame
from gamemode_1.settings import *
from gamemode_1.player import Player
from gamemode_1.background import BG
from gamemode_1.asteroid import Asteroid
from random import randint, choice
from gamemode_1.laser import Laser
from gamemode_1.ui import UI
from global_scripts.button import ButtonGM1
from global_scripts.explosion import Explosion
from gamemode_1.enemy import Enemy

class LevelGM1:
    def __init__(self,screen,quit):

        self.click_sound = pygame.mixer.Sound('global_assets/audio/select.wav')
        self.click_sound.set_volume(0.15)
        
        self.screen = screen
        self.bg = BG()
        self.quit = quit
        self.resume_button = ButtonGM1('resume')
        self.reset_button = ButtonGM1('reset')
        self.exit_button = ButtonGM1('exit')

        self.game_paused = False
        self.pause_type = 'none'
        self.can_pause = True

        player = Player(self.bg.ground_rect.y)
        self.player = pygame.sprite.GroupSingle(player)
        self.explosions = pygame.sprite.Group()

        self.asteroids = pygame.sprite.Group()
        self.last_asteroid = 0
        self.asteroid_cooldown = ASTEROID_COOLDOWN

        self.player_lasers = pygame.sprite.Group()
        self.enemy_lasers = pygame.sprite.Group()
        self.last_laser = 0
        self.laser_cooldown = 2000

        self.score = 0
        self.kills = 0
        self.last_score = 0
        self.score_cooldown = SCORE_COOLDOWN
        self.temp_score = self.score
        self.enemy_score_interval = ENEMY_INTERVAL

        self.ui = UI(100,100,self.score)
        self.enemies = pygame.sprite.Group()
        self.can_spawn = True

        self.music = pygame.mixer.Sound('global_assets/audio/music/music_gm_1.wav')
        self.music_volume = 0.1
        self.music.set_volume(self.music_volume)

        self.laser_sound = pygame.mixer.Sound('global_assets/audio/laser.wav')
        self.laser_sound.set_volume(0.1)

        self.exp_sound = pygame.mixer.Sound('global_assets/audio/explosion_strong.wav')
        self.exp_sound_smol = pygame.mixer.Sound('global_assets/audio/explosion_small.wav')
        self.exp_sound.set_volume(0.1)
        self.exp_sound_smol.set_volume(0.2)

    def create_asteroid(self):
        if pygame.time.get_ticks() - self.last_asteroid >= self.asteroid_cooldown:
            y = HEIGHT - randint(100,HEIGHT-50)
            new_asteroid = Asteroid(randint(0,7),(WIDTH,y))
            self.asteroids.add(new_asteroid)
            self.last_asteroid = pygame.time.get_ticks()

    def asteroid_collisions(self):
        if self.asteroids:
            for asteroid in self.asteroids:
                if pygame.sprite.spritecollide(asteroid,self.player,False):
                    if self.player.sprite.shield > 0:
                        self.player.sprite.shield = 0
                    else:
                        self.player.sprite.health -= 30
                        if self.player.sprite.health <= 0:
                            self.exp_sound.play()
                            self.player.sprite.health = 0
                            self.player.sprite.is_dead = True
                            self.game_paused = True
                            self.pause_type = 'dead'
                            expl = Explosion(self.player.sprite.rect.centerx,self.player.sprite.rect.centery,self.player.sprite.image.get_width()+20)
                            self.explosions.add(expl)
                    asteroid.kill()
                    expl = Explosion(asteroid.rect.centerx,asteroid.rect.centery,asteroid.image.get_width())
                    self.explosions.add(expl)
                    self.exp_sound.play()
                if self.player_lasers:
                    for l in self.player_lasers:
                        if pygame.Rect.colliderect(asteroid.rect,l.rect):
                            l.kill()
                            expl = Explosion(l.rect.centerx,l.rect.centery,l.image.get_width())
                            self.explosions.add(expl)
                            if randint(0,100) == 1:
                                self.score += 50
                                asteroid.kill()
                                expl = Explosion(asteroid.rect.centerx,asteroid.rect.centery,asteroid.image.get_width())
                                self.explosions.add(expl)
                                self.exp_sound.play()
                                self.kills += 1
                            else:
                                self.exp_sound_smol.play()
                
    def input(self):
        mouse = pygame.mouse.get_pressed()

        if mouse[0] and self.can_shoot:
            if self.pause_type == 'none':
                self.can_shoot = False
                new_laser = Laser((self.player.sprite.rect.centerx+100,self.player.sprite.rect.centery+60),1,'player')
                self.player_lasers.add(new_laser)
                self.laser_sound.play()
        elif not mouse[0]:
            self.can_shoot = True

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE] and self.can_pause:
            if not self.game_paused:
                self.game_paused = True
                self.pause_type = 'key'
            elif self.game_paused and not self.pause_type == 'dead':
                self.game_paused = False
                self.pause_type = 'key'
                self.click_sound.play()
            self.can_pause = False
        if not keys[pygame.K_ESCAPE]:
            self.can_pause = True

    def update_score(self):
        if pygame.time.get_ticks() - self.last_score >= self.score_cooldown:
            self.score += 1
            self.last_score = pygame.time.get_ticks()

    def enemy_collisions(self):
        if self.enemies:
            for enemy in self.enemies:
                if pygame.sprite.spritecollide(enemy,self.player_lasers,True):
                    enemy.kill()
                    expl = Explosion(enemy.rect.centerx,enemy.rect.centery,enemy.image.get_width()-30)
                    self.explosions.add(expl)
                    self.score += 10
                    self.exp_sound.play()
                    self.kills += 1

    def enemy_shoot(self):
        if self.enemies and pygame.time.get_ticks() - self.last_laser >= self.laser_cooldown:
            random_enemy = choice(self.enemies.sprites())
            
            new_laser = Laser((random_enemy.rect.centerx,random_enemy.rect.centery),-1,'spaceships')
            self.enemy_lasers.add(new_laser)
            self.laser_sound.play()
            self.last_laser = pygame.time.get_ticks()

    def enemy_laser_collisions(self):
        if self.enemy_lasers:
            for laser in self.enemy_lasers:
                if pygame.sprite.spritecollide(laser,self.player,False):
                    if self.player.sprite.shield:
                        self.player.sprite.shield -= 10
                        if self.player.sprite.shield <= 0:
                            self.player.sprite.shield = 0
                    else:
                        self.player.sprite.health -= 10
                        if self.player.sprite.health <= 0:
                            self.exp_sound.play()
                            self.player.sprite.health = 0
                            self.player.sprite.is_dead = True
                            self.game_paused = True
                            self.pause_type = 'dead'
                            expl = Explosion(self.player.sprite.rect.centerx,self.player.sprite.rect.centery,self.player.sprite.image.get_width()+20)
                            self.explosions.add(expl)
                    laser.kill()
                    expl = Explosion(laser.rect.centerx,laser.rect.centery,laser.image.get_width())
                    self.explosions.add(expl)
                    self.exp_sound_smol.play()

    def create_enemies(self):
        if len(self.enemies) == 0:
            if self.score - self.temp_score >= self.enemy_score_interval:
                x = WIDTH + 200
                y = randint(200,HEIGHT-200)
                type = randint(0,ENEMY_NUM)
                new_enemy = Enemy(type,(x,y))
                self.enemies.add(new_enemy)

                self.temp_score = self.score

    def destroy(self):
        self.player.sprite.health = self.player.sprite.max_health
        self.player.sprite.shield = self.player.sprite.max_shield
        self.player.sprite.is_dead = False
        self.player.sprite.gravity = 0
        self.game_paused = False
        self.pause_type = 'none'
        self.enemies.empty()
        self.enemy_lasers.empty()
        self.asteroids.empty()
        self.player_lasers.empty()
        self.score = 0
        self.kills = 0

    def pause_actions(self):
        if self.pause_type == 'key':
            if self.resume_button.draw(self.screen):
                self.game_paused = False
                self.pause_type = 'none'
                self.click_sound.play()
            if self.exit_button.draw(self.screen):
                self.quit()
                self.click_sound.play()
        if self.pause_type == 'dead':
            if self.reset_button.draw(self.screen):
                self.destroy()
                self.click_sound.play()
            if self.exit_button.draw(self.screen):
                self.quit()
                self.click_sound.play()

    def run(self):

        # other
        self.player.sprite.ground = self.bg.ground_rect.y
        self.input()

        if not self.game_paused:
            pygame.mixer.unpause()
            self.enemy_shoot()
            # cooldowns
            self.create_asteroid()
            self.update_score()
            self.create_enemies()

            # collisions
            self.asteroid_collisions()
            self.enemy_collisions()
            self.enemy_laser_collisions()

            # update
            self.player.update()
            self.asteroids.update()
            self.player_lasers.update()
            self.enemy_lasers.update()
            self.enemies.update()
        
        # draw
        self.explosions.update()
        self.bg.draw_bg(self.screen,self.game_paused)
        if not self.pause_type == 'dead':
            self.player.draw(self.screen)
            self.player_lasers.draw(self.screen)
        self.asteroids.draw(self.screen)
        self.enemy_lasers.draw(self.screen)
        self.enemies.draw(self.screen)
        self.explosions.draw(self.screen)
        self.ui.draw(self.screen,self.player.sprite.health,self.player.sprite.shield,self.player.sprite.max_health,self.player.sprite.max_shield,self.score,self.kills)

        if self.game_paused:
            pygame.mixer.pause()
            self.pause_actions()