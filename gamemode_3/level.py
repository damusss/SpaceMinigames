from tkinter import Widget
import pygame
from settings import *
from gamemode_3.settings import *
from global_scripts.star import Star
from gamemode_3.planet import Planet
from gamemode_3.space_station import SpaceStation
from gamemode_3.meteor import Meteor
from global_scripts.explosion import Explosion
from gamemode_3.fire import GroundFire
from gamemode_3.tanks import Tank
from gamemode_3.weapons import TankBall
from gamemode_3.texts import Text, Message
from gamemode_3.water import Water, SplashAnimation
from gamemode_3.helicopter import Helicopter
from global_scripts.button import ButtonGM3, ButtonGM3PauseActions
from random import randint, choice,uniform
import math

class LevelGM3():
    def __init__(self,screen,quit):

        # sounds
        self.laser_player_sound = pygame.mixer.Sound('global_assets/audio/laser.wav')
        self.laser_player_sound.set_volume(0.1)
        self.laser_army_sound = pygame.mixer.Sound('global_assets/audio/laser.wav')
        self.laser_army_sound.set_volume(0.05)
        self.explosion_smol = pygame.mixer.Sound('global_assets/audio/explosion_small.wav')
        self.explosion_smol.set_volume(0.2)
        self.explosion_big = pygame.mixer.Sound('global_assets/audio/explosion_strong.wav')
        self.explosion_big.set_volume(0.1)
        self.click_sound = pygame.mixer.Sound('global_assets/audio/select.wav')
        self.click_sound.set_volume(0.15)
        self.splash_sound = pygame.mixer.Sound('global_assets/audio/water.wav')
        self.splash_sound.set_volume(0.3)

        # setup
        self.first_time = False
        self.screen = screen
        self.quit = quit
        self.mode = 'shoot'
        self.font_label_buttons = pygame.font.Font('global_assets/font/font_pixel.ttf',18)
        self.info_img = self.font_label_buttons.render('infos:',False,(0,255,255))

        # pause
        self.game_paused = False
        self.pause_type = 'none'
        self.can_pause = True
        self.can_click = True
        self.can_press = True

        # bg
        self.bg = pygame.image.load('gamemode_3/assets/bg/bg.png').convert_alpha()
        self.bg_rect = self.bg.get_rect(bottomleft = (0,HEIGHT))
        self.ground_level = HEIGHT-140

        # station
        self.space_station = SpaceStation(self.ground_level)

        # groups
        self.star_group = pygame.sprite.Group()
        self.planet_group = pygame.sprite.Group()
        self.meteor_group = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.ground_fire_group = pygame.sprite.Group()
        self.tank_group = pygame.sprite.Group()
        self.tank_balls = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.splash_group = pygame.sprite.Group()
        self.messages = pygame.sprite.Group()
        self.helic_group = pygame.sprite.Group()

        # variables
        self.fire_on_base =  0
        self.moneys = 100
        self.max_tanks = 10
        self.army_health = 0
        self.score = 0
        self.last_score = 0
        self.score_cooldown = 1000
        self.max_helics = 5

        # texts
        self.score_text = Text('Score: ',self.score,WIDTH//2,40)
        self.money_text = Text('Moneys: ',self.moneys,30,30)
        text_height = self.money_text.text_rect.inflate(15,15).height
        self.health_text = Text('Base Health: ',self.space_station.health,30,text_height+30+10)
        self.army_num = Text('Tanks Num: ',str(len(self.tank_group))+'/'+str(self.max_tanks),30,text_height*2+30+10+10)
        self.helic_num = Text('Helicopters Num: ',str(len(self.helic_group))+'/'+str(self.max_helics),30,text_height*3+30+10+10+10)
        self.army_health_text = Text('Army Health: ',self.army_health,30,text_height*4+30+10+10+10+10)

        # buttons
        text_height = text_height*5+30+10+10+10+10+10+10
        self.shoot_button = ButtonGM3('shoot','red',WIDTH-30,30,0.5,self.font_label_buttons,'2$',False)
        button_height = self.shoot_button.rect.inflate(15,15).height
        self.tank_button = ButtonGM3('tank','red',WIDTH-30,30+15+button_height,0.5,self.font_label_buttons,'150$',False)
        t_b_h = self.tank_button.rect.inflate(15,15).height
        self.helic_button = ButtonGM3('helic','red',WIDTH-30,30+15+15+button_height+t_b_h,0.5,self.font_label_buttons,'300$',False)
        self.water_button = ButtonGM3('water','red',WIDTH-30,30+15+15+15 +button_height+t_b_h*2,0.5,self.font_label_buttons,'50$',False)
        self.repair_button = ButtonGM3('repair','blue',30,text_height,0.5,self.font_label_buttons,'150$',True,'Repair base','white')
        text_b_h = self.repair_button.rect.inflate(15,15).height
        self.upgrade_base_button = ButtonGM3('upgrade_base','blue',30,text_height+15+text_b_h,0.5,self.font_label_buttons,'200$',True,'upgrade base','white')
        self.upgrade_army_button = ButtonGM3('upgrade_army','blue',30,text_height+15+15+text_b_h*2,0.5,self.font_label_buttons,'250$',True,'upgrade army','white')
        self.delete_fire = ButtonGM3('delete_fire','blue',30,text_height+15+15+15+text_b_h*3,0.5,self.font_label_buttons,'200$',True,'extinguish fires','white')
        self.message_y = self.ground_level-30

        # pause buttons
        self.font = pygame.font.Font('global_assets/font/font_pixel.ttf',35)
        self.font_label = pygame.font.Font('global_assets/font/font_pixel.ttf',25)
        self.resume_button = ButtonGM3PauseActions(WIDTH//2,HEIGHT//2-40,'resume',self.font,(0,255,255),'resume')
        self.exit_button = ButtonGM3PauseActions(WIDTH//2,HEIGHT//2+40,'exit',self.font,'red','exit')
        self.restart_button = ButtonGM3PauseActions(WIDTH//2,HEIGHT//2-30,'restart',self.font,'green','restart')

        # timers
        self.last_meteor = 0
        self.meteor_cooldown = randint(2000,5000)
        self.last_unpause = 0
        self.unpause_cooldown = 100

        # sounds
        self.music = pygame.mixer.Sound('global_assets/audio/music/music_gm_0.wav')

        # startup
        self.create_stars()
        self.create_planets()

    def check_game_over(self):
        if self.space_station.health <= 0:
            self.space_station.health = 0
            self.explosion_big.play()
            expl = Explosion(self.space_station.rect.centerx,self.space_station.rect.centery,self.space_station.image.get_width()-100)
            self.explosions.add(expl)
            message = Message(30,self.message_y,'GAME OVER!','red',10000)
            self.messages.add(message)
            self.game_paused = True
            self.pause_type = 'dead'

    def draw_messages(self):
        if self.messages:
            for index,message in enumerate(self.messages):
                message.draw_message(self.screen,-((message.image.get_height()+10)*index))
                message.update()
            if self.messages:
                self.screen.blit(self.info_img,(30,self.messages.sprites()[-1].rect.top-self.info_img.get_height()-10))

    def draw_buttons(self):
        shoot_color = 'green' if self.mode == 'shoot' else 'red'
        tank_color = 'green' if self.mode == 'tank' else 'red'
        water_color = 'green' if self.mode == 'water' else 'red'
        helic_color = 'green' if self.mode == 'helic' else 'red'
        if self.shoot_button.draw(self.screen,shoot_color):
            if not self.mode == 'shoot':
                self.mode = 'shoot'
            else:
                self.mode = 'none'
            self.click_sound.play()
        if self.tank_button.draw(self.screen,tank_color):
            if not self.mode == 'tank':
                self.mode = 'tank'
            else:
                self.mode = 'none'
            self.click_sound.play()
        if self.water_button.draw(self.screen,water_color):
            if not self.mode == 'water':
                self.mode = 'water'
            else:
                self.mode = 'none'
            self.click_sound.play()
        if self.helic_button.draw(self.screen,helic_color):
            if not self.mode == 'helic':
                self.mode = 'helic'
            else:
                self.mode = 'none'
            self.click_sound.play()
        if self.repair_button.draw(self.screen):
            self.button_buy_actions('repair_base')
            self.click_sound.play()
        if self.upgrade_base_button.draw(self.screen):
            self.button_buy_actions('upgrade_base')
            self.click_sound.play()
        if self.upgrade_army_button.draw(self.screen):
            self.button_buy_actions('upgrade_army')
            self.click_sound.play()
        if self.delete_fire.draw(self.screen):
            self.button_buy_actions('delete_fire')
            self.click_sound.play()

    def button_buy_actions(self,action):
        if action == 'repair_base':
            if self.moneys >= REPAIR_BASE_PRICE:
                self.space_station.health += 500
                if self.space_station.health >= self.space_station.max_health:
                    self.space_station.health = self.space_station.max_health
                self.moneys -= REPAIR_BASE_PRICE
                message = Message(30,self.message_y,'Base repaired by 500 hp (-160$)','green',5000)
                self.messages.add(message)
        elif action == 'upgrade_base':
            if self.moneys >= UPGRADE_BASE_PRICE:
                self.space_station.max_health += 500
                self.moneys -= UPGRADE_BASE_PRICE
                message = Message(30,self.message_y,'Base health upgraded by 500 hp (-200$)','green',5000)
                self.messages.add(message)
        elif action == 'upgrade_army':
            if self.moneys >= UPGRADE_ARMY_PRICE:
                self.max_tanks += TANK_NUM_BONUS
                self.max_helics += HELIC_NUM_BONUS
                if self.tank_group:
                    for t in self.tank_group:
                        t.max_health += TANK_HEALTH_BONUS
                if self.helic_group:
                    for h in self.helic_group:
                        h.max_health += HELIC_HEALTH_BONUS
                self.moneys -= UPGRADE_ARMY_PRICE
                message = Message(30,self.message_y,'Army upgraded +50 hp +2 unities available (-250$)','green',5000)
                self.messages.add(message)
        elif action == 'delete_fire':
            if self.moneys >= EXTINGUISH_FIRES_PRICE and self.ground_fire_group:
                for fire in self.ground_fire_group:
                    fire.kill()
                message = Message(30,self.message_y,f'All fires extinguished ({len(self.ground_fire_group)} fires) (-200$)','green',5000)
                self.messages.add(message)
                self.moneys -= EXTINGUISH_FIRES_PRICE
                self.fire_on_base = 0

    def update_score(self):
        if pygame.time.get_ticks()- self.last_score > self.score_cooldown:
            self.score += 2
            self.last_score = pygame.time.get_ticks()

    def draw_text(self):
        h_color = 'white'
        if self.space_station.health <= 500:
            h_color = 'red'
        elif self.space_station.health <= 2000:
            h_color = 'orange'
        self.score_text.draw_text(self.screen,self.score)
        self.health_text.draw_text(self.screen,str(self.space_station.health)+'/'+str(self.space_station.max_health),h_color)
        self.money_text.draw_text(self.screen,str(self.moneys)+'$')
        self.army_num.draw_text(self.screen,str(len(self.tank_group))+'/'+str(self.max_tanks))
        self.helic_num.draw_text(self.screen,str(len(self.helic_group))+'/'+str(self.max_helics))
        self.army_health_text.draw_text(self.screen,self.army_health)

    def tank_shoot(self):
        if self.moneys >= 0:
            if self.meteor_group:
                for meteor in self.meteor_group:
                    if meteor.rect.x > 20 and meteor.rect.y > 20:
                        if self.tank_group:
                            for tank in self.tank_group:
                                if meteor.rect.centerx - tank.rect.centerx < 400 or meteor.rect.centerx - tank.rect.centerx > -400:
                                    if pygame.time.get_ticks() - tank.last_shoot >= tank.shoot_cooldown and tank.on_ground == True:
                                        x_dist = (meteor.rect.centerx) - tank.rect.centerx
                                        y_dist = -((meteor.rect.centery) - tank.rect.centery)
                                        angle = math.degrees(math.atan2(y_dist, x_dist))
                                        new_ball = TankBall(tank.rect.centerx,tank.rect.centery,angle,'tank')
                                        self.tank_balls.add(new_ball)
                                        tank.last_shoot = pygame.time.get_ticks()
                                        tank.change_image(meteor.rect.x)
                                        self.laser_army_sound.play()

    def helic_shoot(self):
        if self.moneys >= 0:
            if self.meteor_group:
                for meteor in self.meteor_group:
                    if meteor.rect.x > 20 and meteor.rect.y > 20:
                        if self.helic_group:
                            for tank in self.helic_group:
                                if meteor.rect.centerx - tank.rect.centerx < 400 or meteor.rect.centerx - tank.rect.centerx > -400:
                                    if pygame.time.get_ticks() - tank.last_shoot >= tank.shoot_cooldown:
                                        x_dist = (meteor.rect.centerx) - tank.rect.centerx
                                        y_dist = -((meteor.rect.centery) - tank.rect.centery)
                                        angle = math.degrees(math.atan2(y_dist, x_dist))
                                        new_ball = TankBall(tank.rect.centerx,tank.rect.centery,angle,'tank')
                                        self.tank_balls.add(new_ball)
                                        tank.last_shoot = pygame.time.get_ticks()
                                        tank.change_image(meteor.rect.x)
                                        self.laser_army_sound.play()

    def check_tank_death(self):
        if self.tank_group:
            for tank in self.tank_group:
                if tank.is_dead == True:
                    tank.kill()
                    expl = Explosion(tank.rect.centerx,tank.rect.centery,tank.image.get_width()-20)
                    self.explosions.add(expl)
                    message = Message(30,self.message_y,'Tank defeated','red',6000)
                    self.messages.add(message)
                    self.explosion_big.play()

    def check_helic_death(self):
        if self.helic_group:
            for tank in self.helic_group:
                if tank.is_dead == True:
                    tank.kill()
                    expl = Explosion(tank.rect.centerx,tank.rect.centery,tank.image.get_width()-20)
                    self.explosions.add(expl)
                    message = Message(30,self.message_y,'Helicopter defeated','red',6000)
                    self.messages.add(message)
                    self.explosion_big.play()

    def fire_collisions(self):
        if self.ground_fire_group:
            for fire in self.ground_fire_group:
                if fire.rect.bottom > self.ground_level-30:
                    if self.tank_group:
                        for tank in self.tank_group:
                            if tank.rect.colliderect(fire.rect):
                                if pygame.time.get_ticks() - tank.last_damage > tank.damage_cooldown:
                                    tank.health -= FIRE_TO_TANK_DAMAGE
                                    tank.last_damage = pygame.time.get_ticks()
                if self.water_group:
                    for water  in self.water_group:
                        if fire.rect.colliderect(water.rect):
                            water.kill()
                            fire.kill()
                            splash = SplashAnimation(fire.rect.centerx,fire.rect.bottom,'fire')
                            self.splash_group.add(splash)
                            message = Message(30,self.message_y,'Fire extinguished','green',3000)
                            self.messages.add(message)
                            self.fire_on_base -= 1
                            self.splash_sound.play()
                            
        for i in range(self.fire_on_base):
            if pygame.time.get_ticks()- self.space_station.last_damage > self.space_station.damage_cooldown:
                self.space_station.health -= FIRE_TO_BASE_DAMAGE*self.fire_on_base
                self.space_station.last_damage = pygame.time.get_ticks()

        if self.space_station.health <= 0:
            self.space_station.health = 0

    def input(self):
        mouse = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()

        if mouse[0] and self.can_click:
            if not self.game_paused:
                pos = pygame.mouse.get_pos()
                if pos[1] < self.ground_level:
                    if not self.shoot_button.rect.collidepoint(pos[0],pos[1]) and not self.tank_button.rect.collidepoint(pos[0],pos[1]) and not self.water_button.rect.collidepoint(pos[0],pos[1]) and not self.repair_button.rect.collidepoint(pos[0],pos[1]) and not self.upgrade_base_button.rect.collidepoint(pos[0],pos[1]) and not self.helic_button.rect.collidepoint(pos[0],pos[1]) and not self.delete_fire.rect.collidepoint(pos[0],pos[1]):
                        if self.mode == 'tank':
                            if not self.space_station.hitbox_2.left < pos[0] < self.space_station.hitbox_1.right:
                                if len(self.tank_group) < self.max_tanks and self.moneys >= TANK_PRICE:
                                    self.can_click = False
                                    self.spawn_tank(pos)
                                    self.click_sound.play()
                        elif self.mode == 'shoot':
                            if not self.space_station.rect.collidepoint(pos[0],pos[1]):
                                self.shoot_player(pos)
                                self.can_click = False
                                self.click_sound.play()
                        elif self.mode == 'water' and self.moneys >= WATER_PRICE:
                            self.create_water(pos)
                            self.can_click = False
                            self.click_sound.play()
                        elif self.mode == 'helic':
                            if not self.space_station.rect.collidepoint(pos[0],pos[1]):
                                if len(self.helic_group) < self.max_helics and self.moneys >= HELIC_PRICE:
                                    self.can_click = False
                                    self.spawn_helic(pos)
                                    self.click_sound.play()
        if not mouse[0]:
            self.can_click = True

        if self.can_press:
            if keys[pygame.K_1]:
                if not self.mode == 'shoot':
                    self.mode = 'shoot'
                else:
                    self.mode = 'none'
                self.can_press = False
                self.click_sound.play()
            elif keys[pygame.K_2]:
                if not self.mode == 'tank':
                    self.mode = 'tank'
                else:
                    self.mode = 'none'
                self.can_press = False
                self.click_sound.play()
            elif keys[pygame.K_4]:
                if not self.mode == 'water':
                    self.mode = 'water'
                else:
                    self.mode = 'none'
                self.can_press = False
                self.click_sound.play()
            elif keys[pygame.K_3]:
                if not self.mode == 'helic':
                    self.mode = 'helic'
                else:
                    self.mode = 'none'
                self.can_press = False
                self.click_sound.play()

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

        if not any(keys):
            self.can_press = True
            self.can_pause = True

    def create_water(self,pos):
        water = Water(pos[0],pos[1],0.35,self.ground_level)
        self.water_group.add(water)
        self.moneys -= WATER_PRICE
        message = Message(30,self.message_y,f'Bought water (-{WATER_PRICE}$)','green',4000)
        self.messages.add(message)
        self.click_sound.play()

    def shoot_player(self,pos):
        if pygame.time.get_ticks() - self.last_unpause > self.unpause_cooldown:
            x_dist = pos[0] - self.space_station.rect.centerx
            y_dist = -(pos[1] - self.space_station.rect.top)
            angle = math.degrees(math.atan2(y_dist, x_dist))
            new_ball = TankBall(self.space_station.rect.centerx,self.space_station.rect.top,angle,'player')
            self.tank_balls.add(new_ball)
            if self.moneys > BALL_PLAYER_PRICE:
                self.moneys -= BALL_PLAYER_PRICE
            else:
                self.moneys = 0
            self.laser_player_sound.play()

    def get_army_health(self):
        total = 0
        if self.tank_group:
            for t in self.tank_group:
                total += t.health
        if self.helic_group:
            for h in self.helic_group:
                total += h.health
        self.army_health = total

    def spawn_tank(self,pos):
        type = randint(0,TANKS_TYPES)
        new_tank = Tank(pos[0],pos[1],type,self.ground_level)
        self.tank_group.add(new_tank)
        self.moneys-= TANK_PRICE
        message = Message(30,self.message_y,f'Bought new tank (-{TANK_PRICE}$)','green',4000)
        self.messages.add(message)
        self.click_sound.play()

    def spawn_helic(self,pos):
        type = randint(0,HELIC_TYPES)
        new_helic = Helicopter(pos[0],pos[1],type)
        self.helic_group.add(new_helic)
        self.moneys-= HELIC_PRICE
        message = Message(30,self.message_y,f'Bought new helicopter (-{HELIC_PRICE}$)','green',4000)
        self.messages.add(message)
        self.click_sound.play()

    def meteors_collisions(self):
        if self.meteor_group:
            for meteor in self.meteor_group:
                if meteor.rect.collidepoint(meteor.rect.x,self.ground_level):
                    meteor.kill()
                    expl = Explosion(meteor.rect.centerx,meteor.rect.centery,meteor.image.get_width()+20)
                    self.explosions.add(expl)
                    new_fire = GroundFire(meteor.rect.bottomleft[0],meteor.image.get_width()+15,self.ground_level)
                    self.ground_fire_group.add(new_fire)
                    message = Message(30,self.message_y,'New fire lit','yellow',3000)
                    self.messages.add(message)
                    self.explosion_smol.play()
                if meteor.rect.colliderect(self.space_station.hitbox_1):
                    meteor.kill()
                    expl = Explosion(meteor.rect.centerx,meteor.rect.centery,meteor.image.get_width()+20)
                    self.explosions.add(expl)
                    new_fire = GroundFire(meteor.rect.bottomleft[0],meteor.image.get_width()+15,self.space_station.hitbox_1.top)
                    self.ground_fire_group.add(new_fire)
                    self.fire_on_base += 1
                    self.space_station.health -= METEOR_TO_BASE_DAMAGE
                    message = Message(30,self.message_y,f'Base hit by meteor (-{METEOR_TO_BASE_DAMAGE} hp)','orange',5000)
                    self.messages.add(message)
                    self.explosion_big.play()
                if meteor.rect.colliderect(self.space_station.hitbox_2):
                    meteor.kill()
                    expl = Explosion(meteor.rect.centerx,meteor.rect.centery,meteor.image.get_width()+20)
                    self.explosions.add(expl)
                    new_fire = GroundFire(meteor.rect.bottomleft[0],meteor.image.get_width()+15,self.space_station.hitbox_2.top)
                    self.ground_fire_group.add(new_fire)
                    self.fire_on_base += 1
                    self.space_station.health -= METEOR_TO_BASE_DAMAGE
                    message = Message(30,self.message_y,f'Base hit by meteor (-{METEOR_TO_BASE_DAMAGE} hp)','orange',5000)
                    self.messages.add(message)
                    self.explosion_big.play()
                if self.tank_group:
                    for tank in self.tank_group:
                        if meteor.rect.colliderect(tank.rect)and tank.on_ground:
                            meteor.kill()
                            expl = Explosion(meteor.rect.centerx,meteor.rect.centery,meteor.image.get_width()+20)
                            self.explosions.add(expl)
                            tank.health -= METEOR_TO_TANK_DAMAGE
                            message = Message(30,self.message_y,'Tank hit by meteor','orange',5000)
                            self.messages.add(message)
                            self.explosion_big.play()
                if self.helic_group:
                    for tank in self.helic_group:
                        if meteor.rect.colliderect(tank.rect):
                            meteor.kill()
                            expl = Explosion(meteor.rect.centerx,meteor.rect.centery,meteor.image.get_width()+20)
                            self.explosions.add(expl)
                            tank.health -= METEOR_TO_HELIC_DAMAGE
                            message = Message(30,self.message_y,'Helicopter hit by meteor','orange',5000)
                            self.messages.add(message)
                            self.explosion_big.play()
                if self.tank_balls:
                    for ball in self.tank_balls:
                        if meteor.rect.colliderect(ball.hitbox):
                            meteor.kill()
                            ball.kill()
                            expl = Explosion(meteor.rect.centerx,meteor.rect.centery,meteor.image.get_width()+20)
                            self.explosions.add(expl)
                            self.moneys += 10
                            self.score += 5
                            self.explosion_smol.play()

    def spawn_meteors(self):
        if pygame.time.get_ticks() - self.last_meteor >= self.meteor_cooldown:
            r_x = randint(-200,WIDTH+200)
            y = -200
            r_type = randint(0,METEOR_TYPES)
            r_x_target = randint(100,WIDTH-100)
            y_target = self.ground_level
            r_scale = uniform(METEOR_SCALES[0],METEOR_SCALES[1])
            new_meteor = Meteor(r_x,y,r_type,r_scale,r_x_target,y_target)
            self.meteor_group.add(new_meteor)
            self.last_meteor = pygame.time.get_ticks()
            self.meteor_cooldown = randint(2000,5000)

    def create_planets(self):
        while len(self.planet_group) < PLANET_NUM:
            r_x = randint(100,WIDTH-100)
            r_y = randint(100,HEIGHT-self.bg.get_height()-300)
            r_scale = uniform(PLANET_SCALES[0],PLANET_SCALES[1])
            r_type = randint(0,PLANET_NUM)
            new_planet = Planet(r_type,r_scale,r_x,r_y)
            self.planet_group.add(new_planet)

    def create_stars(self):
        while len(self.star_group) < STARS_NUM:
            random_x = randint(0,WIDTH)
            random_y = randint(0,HEIGHT)
            random_size = choice(STAR_SIZES)
            new_star = Star(random_x,random_y,random_size)
            self.star_group.add(new_star)

    def destroy(self):
        self.first_time = True
        self.planet_group.empty()
        self.star_group.empty()
        self.tank_group.empty()
        self.explosions.empty()
        self.tank_balls.empty()
        self.meteor_group.empty()
        self.water_group.empty()
        self.splash_group.empty()
        self.ground_fire_group.empty()
        self.helic_group.empty()
        self.messages.empty()
        self.moneys = 100
        self.score = 0
        self.max_tanks = 10
        self.max_helics = 5
        self.army_health = 0
        self.space_station.max_health = 5000
        self.game_paused = False
        self.pause_type = 'none'

    def pause_actions(self):
        if self.pause_type == 'key':
            label = self.font_label.render('pause',False,'yellow')
            label_r = label.get_rect(center = (WIDTH//2,self.resume_button.rect.top-50))
            if self.resume_button.draw(self.screen):
                self.game_paused = False
                self.pause_type = 'none'
                self.last_unpause = pygame.time.get_ticks()
            if self.exit_button.draw(self.screen):
                self.quit()
            self.screen.blit(label,label_r)
        elif self.pause_type == 'dead':
            label = self.font_label.render('game over!',False,'yellow')
            label_r = label.get_rect(center = (WIDTH//2,self.restart_button.rect.top-50))
            if self.restart_button.draw(self.screen):
                self.destroy()
                self.recreate()
                self.game_paused = False
                self.pause_type = 'none'
            if self.exit_button.draw(self.screen):
                self.quit()
            self.screen.blit(label,label_r)

    def recreate(self):
        self.create_planets()
        self.create_stars()
        self.moneys = 102

    def run(self):
        # bg
        self.screen.fill('black')
        self.star_group.update(self.screen)
        self.screen.blit(self.bg,self.bg_rect)
        self.screen.blit(self.bg,(self.bg_rect.x+self.bg.get_width(),self.bg_rect.y))
        self.planet_group.draw(self.screen)
        self.input()

        if not self.game_paused:
            pygame.mixer.unpause()
            # update
            self.helic_shoot()
            self.check_helic_death()
            self.update_score()
            self.get_army_health()
            self.check_tank_death()
            self.fire_collisions()
            self.tank_shoot()
            self.meteors_collisions()
            self.spawn_meteors()
            self.meteor_group.update(self.screen)
            self.ground_fire_group.update()
            self.tank_group.update(self.screen)
            self.tank_balls.update()
            self.water_group.update(self.screen)
            self.splash_group.update()
            self.helic_group.update(self.screen)
            self.check_game_over()

        # draw
        if not self.pause_type == 'dead':self.space_station.draw(self.screen)
        self.meteor_group.draw(self.screen)
        self.explosions.update()
        self.tank_balls.draw(self.screen)
        self.tank_group.draw(self.screen)
        self.helic_group.draw(self.screen)
        self.ground_fire_group.draw(self.screen)
        self.water_group.draw(self.screen)
        self.splash_group.draw(self.screen)
        self.explosions.draw(self.screen)
        self.draw_buttons()
        self.draw_text()
        self.draw_messages()

        if self.game_paused:
            pygame.mixer.pause()
            self.pause_actions()

        if self.moneys <= 0:
            self.moneys = 0