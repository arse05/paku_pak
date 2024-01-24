import pygame
from pygame.sprite import Sprite

class Enemy(Sprite):
    def __init__(self, screen):
        super(Enemy, self).__init__()
        self.screen = screen
        self.image = pygame.image.load("images/enemy.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.x = 600
        self.rect.y = self.screen_rect.centery - 40
        self.moving = False
        self.weakness = False
        self.horizontal = True
        self.die = False

    def update (self):
        if ((self.rect.x > 750 or self.rect.x < 0) and self.weakness) or self.die:
            pass
        else:
            if self.moving and self.weakness == False:
                self.rect.x += 4
            elif self.moving == 0 and self.weakness == False:
                self.rect.x -= 4
            if self.moving and self.weakness == True:
                self.rect.x -= 4
            elif self.moving == 0 and self.weakness == True:
                self.rect.x += 4

    def flip_image(self, horizontal=False, vertical=False):
        self.image = pygame.transform.flip(self.image, horizontal, vertical)