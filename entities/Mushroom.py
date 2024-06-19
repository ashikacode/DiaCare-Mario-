import pygame
from classes.Animation import Animation
from classes.Maths import Vec2D
from entities.EntityBase import EntityBase
from traits.leftrightwalk import LeftRightWalkTrait
from classes.Collider import Collider
from classes.EntityCollider import EntityCollider


class RedMushroom(EntityBase):
    def __init__(self, screen, spriteColl, x, y, level, sound):
        super(RedMushroom, self).__init__(y, x - 1, 1.25)
        self.spriteCollection = spriteColl
        self.animation = Animation(
            [
                self.spriteCollection.get("mushroom").image,
            ]
        )
        self.screen = screen
        self.leftrightTrait = LeftRightWalkTrait(self, level)
        self.type = "Mob"
        self.dashboard = level.dashboard
        self.collision = Collider(self, level)
        self.EntityCollider = EntityCollider(self)
        self.levelObj = level
        self.sound = sound

    def update(self, camera):
        if self.alive:
            self.applyGravity()
            self.drawRedMushroom(camera)
            self.leftrightTrait.update()
            self.checkEntityCollision()
        else:
            self.onDead(camera)

    def drawRedMushroom(self, camera):
        self.anIm = pygame.image.load('./img/icons/Insulin.png').convert_alpha()
        self.anIm_scale = pygame.transform.scale(self.anIm, (32*1.5, 32*1.1))
        self.screen.blit(self.anIm_scale, (self.rect.x + camera.x, self.rect.y))
        # self.screen.blit(self.animation.image, (self.rect.x + camera.x, self.rect.y))
        self.animation.update()

    def onDead(self, camera):
        if self.timer == 0:
            self.setPointsTextStartPosition(self.rect.x + 3, self.rect.y)
        if self.timer < self.timeAfterDeath:
            self.movePointsTextUpAndDraw(camera)
        else:
            self.alive = None
        self.timer += 0.1

    def setPointsTextStartPosition(self, x, y):
        self.textPos = Vec2D(x, y)

    def movePointsTextUpAndDraw(self, camera):
        self.textPos.y += -0.5
        self.dashboard.drawText("INSULIN+++", self.textPos.x + camera.x +10, self.textPos.y-10, 8)

    def checkEntityCollision(self):
        pass
