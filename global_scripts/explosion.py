import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y,size_width):
        pygame.sprite.Sprite.__init__(self)

        self.size_width = size_width
        self.images = self.import_images()
        self.image = self.images[0]
        self.rect = self.image.get_rect(center = (x,y))
        self.frame_index = 0
        self.speed = 0.25

    def import_images(self):
        images = []
        for i in range(5):
            img = pygame.image.load(f'global_assets/images/explosion/frame_{i}.png').convert_alpha()
            img = pygame.transform.scale(img,(int(self.size_width),int(self.size_width)))
            images.append(img)
        return images

    def animate(self):
        self.frame_index += self.speed
        self.image = self.images[int(self.frame_index)]
        if self.frame_index >= len(self.images)-1:
            self.kill()

    def update(self):
        self.animate()