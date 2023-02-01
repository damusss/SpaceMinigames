import pygame
from gamemode_2.player import Player
import gamemode_2.obstacle as obstacle
from gamemode_2.alien import Alien, Extra
from random import choice, randint
from gamemode_2.laser import Laser
from global_scripts.button import ButtonGM2
from global_scripts.explosion import Explosion
from settings import *

class LevelGM2:
    def __init__(self,screen,quit):

        self.click_sound = pygame.mixer.Sound('global_assets/audio/select.wav')
        self.click_sound.set_volume(0.15)
        
        self.toggle_old_style = True
        self.screen = screen
        self.quit = quit
        self.crt = CRT(self.screen)
        self.first_time = False

        #pause
        self.game_paused = False
        self.pause_type = 'none'
        self.can_pause = True
        
        # player
        self.laser_sound = pygame.mixer.Sound('global_assets/audio/laser.wav')
        self.laser_sound.set_volume(0.1)
        player_sprite = Player((WIDTH / 2,HEIGHT - 10), WIDTH,5,self.laser_sound)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # health and score
        self.lives = 3
        self.live_surf = pygame.image.load('gamemode_2/assets/player.png').convert_alpha()
        self.live_x_start_pos = WIDTH -(self.live_surf.get_size()[0]*2+20)
        self.score = 0
        self.font = pygame.font.Font('global_assets/font/font_pixel_2.ttf',20)
        self.kills = 0

        # buttons
        self.exit_button = ButtonGM2('exit',self.font)
        self.resume_button = ButtonGM2('resume',self.font)
        self.retry_button = ButtonGM2('reset',self.font)
        self.restart_button = ButtonGM2('win',self.font)
        self.toggle_button = ButtonGM2('toggle',self.font)

        # obstacle
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 8
        self.obstacle_x_positions = [num * (WIDTH/self.obstacle_amount)for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions,x_start=WIDTH/15 - 18,y_start=HEIGHT-180)

        # alien
        self.aliens = pygame.sprite.Group()
        self.alien_setup(rows=12,cols=20)
        self.default_direction = 2
        self.alien_direction = self.default_direction
        self.alien_lasers = pygame.sprite.Group()

        # extra
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(800,1200)
        self.shoot_time = randint(20,60)

        # audio
        self.music = pygame.mixer.Sound('global_assets/audio/music/music_gm_2.wav')
        self.music_volume = 0.1
        self.music.set_volume(self.music_volume)
        self.explosion_sound = pygame.mixer.Sound('global_assets/audio/explosion_small.wav')
        self.explosion_sound.set_volume(0.2)

        self.explosions = pygame.sprite.Group()

    def create_obstacle(self, x_start,y_start,offset_x):
        for row_index,row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    # (241,79,80)
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size,(220,0,220),x,y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self,*offset,x_start,y_start):
        for offset_x in offset:
            self.create_obstacle(x_start,y_start,offset_x)

    def alien_setup(self,rows,cols,x_distance=60,y_distance=48, x_offset=130,y_offset=80):
        for row_index,row in enumerate(range(rows)):
            for col_index,col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0: alien_sprite = Alien('yellow',x,y)
                elif 1 <= row_index <= 3: alien_sprite = Alien('green',x,y)
                else: alien_sprite = Alien('red',x,y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= WIDTH:
                self.alien_direction = -self.default_direction
                self.alien_move_down(1)
            elif alien.rect.left <= 0:
                self.alien_direction = self.default_direction
                self.alien_move_down(1)

    def alien_move_down(self,distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens:
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center,'white',12,HEIGHT)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right','left']),WIDTH))
            self.extra_spawn_time = randint(800,1200)

    def alien_shoot_timer(self):
        self.shoot_time -= 1
        if self.shoot_time <= 0:
            self.alien_shoot()
            self.shoot_time = randint(20,60)

    def collision_checks(self):

        # player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # obstacle
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                    expl = Explosion(laser.rect.centerx,laser.rect.centery,laser.image.get_height())
                    self.explosions.add(expl)

                # alien
                aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                        expl = Explosion(alien.rect.centerx,alien.rect.centery,alien.image.get_width())
                        self.explosions.add(expl)
                        self.kills += 1
                    aliens_hit.clear()
                    laser.kill()
                    self.explosion_sound.play()

                # extra
                if pygame.sprite.spritecollide(laser,self.extra,True):
                    laser.kill()
                    self.score += 100
                    expl = Explosion(self.extra.sprites()[0].rect.centerx,self.extra.sprites()[0].rect.centery,self.extra.sprites()[0].image.get_width())
                    self.explosions.add(expl)

        # alien lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # obstacle
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                    expl = Explosion(laser.rect.centerx,laser.rect.centery,laser.image.get_height())
                    self.explosions.add(expl)

                if pygame.sprite.spritecollide(laser,self.player,False):
                    laser.kill()
                    self.lives -= 1
                    expl = Explosion(laser.rect.centerx,laser.rect.centery,laser.image.get_height())
                    self.explosions.add(expl)
                    if self.lives <= 0:
                        self.lives = 0
                        self.game_paused = True
                        self.pause_type = 'dead'
                        expl = Explosion(self.player.sprite.rect.centerx,self.player.sprite.rect.centery,self.player.sprite.image.get_width())
                        self.explosions.add(expl)

        # aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks,True)
                if pygame.sprite.spritecollide(alien,self.player,False):
                    self.game_paused = True
                    self.pause_type = 'dead'

    def display_lives(self):
        for live in range(self.lives-1):
            x = self.live_x_start_pos+ (live*(self.live_surf.get_size()[0]+10))
            self.screen.blit(self.live_surf,(x,8))

    def display_score(self):
        score_surf = self.font.render(f'SCORE: {self.score}',False,'white')
        score_rect = score_surf.get_rect(topleft= (10,-10))
        self.screen.blit(score_surf,score_rect)
        kills_surf = self.font.render(f'KILLS: {self.kills}',False,'white')
        kills_rect = kills_surf.get_rect(topleft= (10,27))
        self.screen.blit(kills_surf,kills_rect)

    def victory(self):
        if not self.aliens.sprites():
            self.game_paused = True
            self.pause_type = 'win'

    def pause_actions(self):
        if self.pause_type == 'win':
            victory_s = self.font.render('You Won!',False,'white')
            victory_r = victory_s.get_rect(center = (WIDTH//2,HEIGHT//2-150))
            self.screen.blit(victory_s,victory_r)
            if self.restart_button.draw(self.screen):
                self.destroy()
                self.recreate()
                self.click_sound.play()
            if self.exit_button.draw(self.screen):
                self.quit()
                self.click_sound.play()
        if self.pause_type == 'dead':
            victory_s = self.font.render('Game Over!',False,'white')
            victory_r = victory_s.get_rect(center = (WIDTH//2,HEIGHT//2-150))
            self.screen.blit(victory_s,victory_r)
            if self.retry_button.draw(self.screen):
                self.destroy()
                self.recreate()
                self.click_sound.play()
            if self.exit_button.draw(self.screen):
                self.quit()
                self.click_sound.play()
        if self.pause_type == 'key':
            victory_s = self.font.render('Pause',False,'white')
            victory_r = victory_s.get_rect(center = (WIDTH//2,HEIGHT//2-150))
            self.screen.blit(victory_s,victory_r)
            if self.resume_button.draw(self.screen):
                self.pause_type = 'none'
                self.game_paused = False
                self.click_sound.play()
            if self.exit_button.draw(self.screen):
                self.quit()
                self.click_sound.play()
            if self.toggle_button.draw(self.screen):
                self.toggle_old_style = not self.toggle_old_style

    def destroy(self):
        self.blocks.empty()
        self.aliens.empty()
        self.alien_lasers.empty()
        self.extra.empty()
        self.player.sprite.lasers.empty()
        self.game_paused = False
        self.pause_type = 'none'
        self.score = 0
        self.lives = 3
        self.kills = 0
        self.player.sprite.rect.centerx = WIDTH//2
        self.toggle_old_style = True
        self.first_time = True

    def recreate(self):
        self.create_multiple_obstacles(*self.obstacle_x_positions,x_start=WIDTH/15 - 18,y_start=HEIGHT-180)
        self.alien_setup(rows=12,cols=20)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            if not self.game_paused:
                if self.can_pause:
                    self.game_paused = True
                    self.pause_type = 'key'
                    self.can_pause = False
            if self.game_paused and self.pause_type == 'key' and self.can_pause:
                self.game_paused = False
                self.pause_type = 'none'
                self.can_pause = False
                self.click_sound.play()
        if not keys[pygame.K_ESCAPE]:
            self.can_pause = True

    def run(self):
        # bg
        self.screen.fill((30,30,30))
        # input
        self.input()

        if not self.game_paused:
            pygame.mixer.unpause()
            # updates
            self.alien_shoot_timer()
            self.collision_checks()
            self.extra_alien_timer()
            self.extra.update()
            self.player.update()
            self.alien_position_checker()
            self.aliens.update(self.alien_direction)
            self.alien_lasers.update()
        # draws
        self.player.draw(self.screen)
        self.blocks.draw(self.screen)
        self.aliens.draw(self.screen)
        self.player.sprite.lasers.draw(self.screen)
        self.alien_lasers.draw(self.screen)
        self.extra.draw(self.screen)
        self.display_lives()
        self.display_score()
        self.victory()
        self.explosions.update()
        self.explosions.draw(self.screen)
        if self.toggle_old_style:
            self.crt.draw()
        if self.game_paused:
            pygame.mixer.pause()
            self.pause_actions()

class CRT:
    def __init__(self,screen):
        self.tv = pygame.image.load('gamemode_2/assets/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv,(int(WIDTH),int(HEIGHT)))
        self.screen = screen

    def draw(self):
        self.tv.set_alpha(randint(60,100))
        self.screen.blit(self.tv,(0,0))
        self.create_lines()

    def create_lines(self):
        line_height = 3
        line_amount = int(HEIGHT/line_height)
        for line in range(line_amount):
            y_pos = line*line_height
            pygame.draw.line(self.tv,'black',(0,y_pos),(WIDTH,y_pos),1)