from copy import copy

from entities.EntityBase import EntityBase


class Flag(EntityBase):
    def __init__(self, screen, spriteCollection, x, y, gravity=0):
        super(Flag, self).__init__(x, y, gravity)
        self.screen = screen
        self.spriteCollection = spriteCollection
        self.animation = copy(self.spriteCollection.get("flag").animation)
        self.type = "End"

    def update(self, cam):
        if self.alive:
            self.animation.update()
            self.screen.blit(self.animation.image, (self.rect.x + cam.x, self.rect.y))
