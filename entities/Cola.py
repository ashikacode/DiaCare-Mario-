from copy import copy

import pygame

from entities.EntityBase import EntityBase


class Cola(EntityBase):
    def __init__(self, screen, spriteCollection, x, y, gravity=0):
        super(Cola, self).__init__(x, y, gravity)
        self.screen = screen
        self.spriteCollection = spriteCollection
        self.animation = copy(self.spriteCollection.get("coke").animation)
        self.anIm = pygame.image.load('./img/cola.png').convert_alpha()
        self.anIm_scale = pygame.transform.scale(self.anIm, (32, 32))

        self.type = "Item"

    def update(self, cam):
        if self.alive:
            self.animation.update()
            self.screen.blit(self.anIm_scale, (self.rect.x + cam.x, self.rect.y))
            # self.screen.blit(self.animation.image, (self.rect.x + cam.x, self.rect.y))
