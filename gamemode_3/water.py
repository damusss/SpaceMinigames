import pygame

class Water(pygame.sprite.Sprite):
    def __init__(self,x,y,scale,ground):
        pygame.sprite.Sprite.__init__(self)

        self.ground = ground
        self.image = pygame.image.load(f'gamemode_3/assets/water/water.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(int(self.image.get_width()*scale),int(self.image.get_height()*scale)))
        self.rect = self.image.get_rect(center = (x,y))
        self.gravity_start = 0.5
        self.gravity = 0
        self.on_ground = False
        self.animation = pygame.sprite.Group()
        self.is_on_ground = False
        self.splash_sound = pygame.mixer.Sound('global_assets/audio/water.wav')
        self.splash_sound.set_volume(0.3)

    def fall(self):
        self.gravity += self.gravity_start
        self.rect.y += self.gravity

    def check_death(self):
        if self.on_ground:
            self.image.set_alpha(0)
            splash = SplashAnimation(self.rect.x,self.ground)
            self.animation.add(splash)
            self.is_on_ground = True
            self.splash_sound.play()

    def update(self,screen):
        if self.rect.bottom < self.ground:
            self.fall()
        elif self.rect.bottom > self.ground:
            self.rect.bottom = self.ground
            self.gravity = 0
            self.on_ground = True
        else:
            self.gravity = 0
            self.on_ground = True

        if not self.is_on_ground:
            self.check_death()

        self.animation.draw(screen)
        self.animation.update()

        for a in self.animation:
            if a.is_dead == True:
                a.kill()
                self.kill()

class SplashAnimation(pygame.sprite.Sprite):
    def __init__(self,x,y,who='water'):
        pygame.sprite.Sprite.__init__(self)

        self.images = self.import_images()
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom = (x,y))
        self.frame_index = 0
        self.speed = 0.7
        self.is_dead = False
        self.check = False
        if who != 'water':
            self.check = True

    def import_images(self):
        images = []
        for i in range(0,21):
            img = pygame.image.load(f'gamemode_3/assets/water/splash/{i}.png').convert_alpha()
            scale = 0.1
            img = pygame.transform.scale(img,(int(img.get_width()*scale),int(img.get_height()*scale)))
            images.append(img)
        return images

    def animate(self):
        self.frame_index += self.speed
        if not self.is_dead:
            self.image = self.images[int(self.frame_index)]
        if self.frame_index >= len(self.images)-1:
            if self.check == False:
                self.is_dead = True
            else:
                self.kill()

    def update(self):

        self.animate()