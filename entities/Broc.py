from copy import copy

import pygame

from entities.EntityBase import EntityBase


class Broc(EntityBase):
    def __init__(self, screen, spriteCollection, x, y, gravity=0):
        super(Broc, self).__init__(x, y, gravity)
        self.screen = screen
        self.spriteCollection = spriteCollection
        self.animation = copy(self.spriteCollection.get("broc").animation)
        self.type = "Item"

        # Load all images and scale them
        self.images = [
            pygame.transform.scale(pygame.image.load('./img/icons/Brocolli.png').convert_alpha(), (32, 32)),
            pygame.transform.scale(pygame.image.load('./img/icons/Brocolli1.png').convert_alpha(), (32, 32)),
            pygame.transform.scale(pygame.image.load('./img/icons/Brocolli2.png').convert_alpha(), (32, 32))
        ]
        self.current_image = 0  # Start with the first image
        self.image_timer = 0  # Timer to track when to switch images
        self.image_switch_interval = 250  # Time in milliseconds to switch images

    def update(self, cam):
        if self.alive:
            self.animation.update()
            # Manage image switching based on time
            current_time = pygame.time.get_ticks()  # Get current time in milliseconds
            if current_time - self.image_timer >= self.image_switch_interval:
                self.image_timer = current_time  # Reset timer
                self.current_image = (self.current_image + 1) % len(self.images)  # Move to the next image, loop back to first
            
            # Blit the current image
            self.screen.blit(self.images[self.current_image], (self.rect.x + cam.x, self.rect.y))
            # self.screen.blit(self.animation.image, (self.rect.x + cam.x, self.rect.y))
