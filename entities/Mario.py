import pygame

from classes.Animation import Animation
from classes.Camera import Camera
from classes.Collider import Collider
from classes.EntityCollider import EntityCollider
from classes.Input import Input
from classes.Sprites import Sprites
from entities.EntityBase import EntityBase
from entities.Mushroom import RedMushroom
from traits.bounce import bounceTrait
from traits.go import GoTrait
from traits.jump import JumpTrait
from classes.Pause import Pause

spriteCollection = Sprites().spriteCollection
smallAnimation = Animation(
    [
        spriteCollection["mario_run1"].image,
        spriteCollection["mario_run2"].image,
        spriteCollection["mario_run3"].image,
    ],
    spriteCollection["mario_idle"].image,
    spriteCollection["mario_jump"].image,
)
bigAnimation = Animation(
    [
        spriteCollection["mario_big_run1"].image,
        spriteCollection["mario_big_run2"].image,
        spriteCollection["mario_big_run3"].image,
    ],
    spriteCollection["mario_big_idle"].image,
    spriteCollection["mario_big_jump"].image,
)


class Mario(EntityBase):
    def __init__(self, x, y, level, screen, dashboard, sound, gravity=0.8):
        super(Mario, self).__init__(x, y, gravity)
        self.levelObj = level
        self.camera = Camera(self.rect, self, self.levelObj.levelLength)
        self.sound = sound
        self.dashboard = dashboard
        self.screen = screen
        self.input = Input(self,self.dashboard,self.screen)
        self.inAir = False
        self.inJump = False
        self.powerUpState = 0
        self.invincibilityFrames = 0
        self.traits = {
            "jumpTrait": JumpTrait(self,dashboard),
            "goTrait": GoTrait(smallAnimation, screen, self.camera, self,dashboard),
            "bounceTrait": bounceTrait(self),
        }
        self.end_image_original = pygame.image.load('./img/Ending screen.png').convert_alpha()
        self.end_image_original1 = pygame.image.load('./img/Ending screen 1.png').convert_alpha()

        # Set the desired dimensions for the end-level image
        desired_width = 400  # Set to your desired width
        desired_height = 300  # Set to your desired height
        
        # Scale the image to the desired dimensions
        self.end_image = pygame.transform.scale(self.end_image_original, (desired_width, desired_height))
        self.end_image_rect = self.end_image.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))

        self.end_image1 = pygame.transform.scale(self.end_image_original1, (desired_width, desired_height))
        self.end_image_rect1 = self.end_image1.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))


        
        self.collision = Collider(self, level)
        
        self.EntityCollider = EntityCollider(self)
        
        self.restart = False
        self.pause = False
        self.pauseObj = Pause(screen, self, dashboard)
        self.speed = False

        self.isWarning = True

    def update(self):
        if self.invincibilityFrames > 0:
            self.invincibilityFrames -= 1
        self.updateTraits()
        self.moveMario()
        self.camera.move()
        self.applyGravity()
        self.checkEntityCollision()
        self.input.checkForInput()

    def moveMario(self):
        self.rect.y += self.vel.y
        self.collision.checkY()
        self.rect.x += self.vel.x
        self.collision.checkX()

    def checkEntityCollision(self):
        for ent in self.levelObj.entityList:
            collisionState = self.EntityCollider.check(ent)
            if collisionState.isColliding:
                if ent.type == "Item":
                    self._onCollisionWithItem(ent)
                elif ent.type == "Block":
                    self._onCollisionWithBlock(ent)
                elif ent.type == "Mob":
                    self._onCollisionWithMob(ent, collisionState)
                elif ent.type == "Unhealthy":
                    self._onCollisionWithUnhealthy(ent)
                elif ent.type == "End":
                    self._onCollisionWithEnd(ent)
    
    # apple or grapes or brocoli
    def _onCollisionWithItem(self, item):
        # if item.name == "broc":
        #     self.show_text_animation("Healthy", self.getPos())
        # if item.name == "coke":
        #     self.show_text_animation("Unhealthy", self.getPos())
        self.levelObj.entityList.remove(item)
        if self.dashboard.points <= 2000:
            self.dashboard.points += 100
        if self.dashboard.points1 <= 2000:
            self.dashboard.points1 += 100
        self.dashboard.coins += 1
        self.sound.play_sfx(self.sound.coin)

    def _onCollisionWithEnd(self, item):
        self.levelObj.entityList.remove(item)
        self.sound.play_sfx(self.sound.powerup)

        # Correctly display the image based on the score
        if self.dashboard.points > 1200:
            self.screen.blit(self.end_image1, self.end_image_rect1)
        elif self.dashboard.points >= 800:
            self.screen.blit(self.end_image, self.end_image_rect)
        else:
            self.screen.blit(self.end_image1, self.end_image_rect1)  # Default case, can adjust as needed

        pygame.display.update()
        pygame.time.wait(2000)  # Pause for 2000 milliseconds (2 seconds)
        self.restart = True


    def _onCollisionWithUnhealthy(self, item):
        self.levelObj.entityList.remove(item)
        if self.dashboard.points >= 150:
            self.dashboard.points -= 150
        self.dashboard.coins -= 1
        self.sound.play_sfx(self.sound.kick)
        # self.dashboard.drawText("-100", self.rect.x + self.camera.x, self.rect.y, 8)


    def show_text_animation(self, text, position):
        font = pygame.font.Font(None, 36)  # Use appropriate font and size
        text_surface = font.render(text, True, (255, 255, 255))  # White text for visibility
        text_rect = text_surface.get_rect(center=(position[0], position[1] - 20))  # Adjust position as needed

        # Display the text for a few frames
        for _ in range(30):  # Show text for 30 frames, adjust as needed for timing
            self.screen.blit(text_surface, text_rect)
            pygame.display.update()
            pygame.time.delay(33)  # Delay to control the speed of the animation


    def _onCollisionWithBlock(self, block):
        if not block.triggered:
            self.dashboard.coins += 1
            self.sound.play_sfx(self.sound.bump)
            if self.dashboard.points1 >= 200:
                self.dashboard.points1 -= 200
            if self.dashboard.points >= 200:
                self.dashboard.points -= 200
            # self.powerup(1)
        block.triggered = True

    # burger or coke
    def _onCollisionWithMob(self, mob, collisionState):
        if self.isWarning and not isinstance(mob, RedMushroom):
            self.pause = True
            self.pauseObj.onlyContinue = True
            self.pauseObj.createBackgroundBlur()
            self.isWarning = False
        if isinstance(mob, RedMushroom) and mob.alive:
            self.powerup(1)
            if self.dashboard.points1 >= 350:
                self.dashboard.points1 -= 350
            if self.dashboard.points <= 2000:
                self.dashboard.points += 100
            self.killEntity(mob)
            self.sound.play_sfx(self.sound.powerup)
        elif collisionState.isTop and (mob.alive or mob.bouncing):
            self.sound.play_sfx(self.sound.stomp)
            self.rect.bottom = mob.rect.top
            self.bounce()
            self.killEntity(mob)
        elif collisionState.isTop and mob.alive and not mob.active:
            self.sound.play_sfx(self.sound.stomp)
            self.rect.bottom = mob.rect.top
            mob.timer = 0
            self.bounce()
            mob.alive = False
        elif collisionState.isColliding and mob.alive and not mob.active and not mob.bouncing:
            mob.bouncing = True
            if mob.rect.x < self.rect.x:
                mob.leftrightTrait.direction = -1
                mob.rect.x += -5
                self.sound.play_sfx(self.sound.kick)
            else:
                mob.rect.x += 5
                mob.leftrightTrait.direction = 1
                self.sound.play_sfx(self.sound.kick)
        elif collisionState.isColliding and mob.alive and not self.invincibilityFrames:
            if self.powerUpState == 0:
                self.sound.play_sfx(self.sound.stomp)
                self.killEntity(mob)
                # self.gameOver()
                self.speed = True
                print("gameover")
            elif self.powerUpState == 1:
                self.powerUpState = 0
                self.traits['goTrait'].updateAnimation(smallAnimation)
                x, y = self.rect.x, self.rect.y
                self.rect = pygame.Rect(x, y + 32, 32, 32)
                self.invincibilityFrames = 60
                self.sound.play_sfx(self.sound.pipe)

    def bounce(self):
        self.traits["bounceTrait"].jump = True

    def killEntity(self, ent):
        if ent.__class__.__name__ != "Koopa":
            ent.alive = False
        else:
            # ent.timer = 0
            # ent.leftrightTrait.speed = 1
            # ent.alive = True
            # ent.active = False
            # ent.bouncing = False
            ent.alive = False
        if self.dashboard.points <= 2000:
            self.dashboard.points += 200

    def gameOver(self):
        srf = pygame.Surface((640, 480))
        srf.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        srf.set_alpha(128)
        self.sound.music_channel.stop()
        self.sound.music_channel.play(self.sound.death)

        for i in range(500, 20, -2):
            srf.fill((0, 0, 0))
            pygame.draw.circle(
                srf,
                (255, 255, 255),
                (int(self.camera.x + self.rect.x) + 16, self.rect.y + 16),
                i,
            )
            self.screen.blit(srf, (0, 0))
            pygame.display.update()
            self.input.checkForInput()
        while self.sound.music_channel.get_busy():
            pygame.display.update()
            self.input.checkForInput()
        self.restart = True

    def getPos(self):
        return self.camera.x + self.rect.x, self.rect.y

    def setPos(self, x, y):
        self.rect.x = x
        self.rect.y = y
        
    def powerup(self, powerupID):
        if self.powerUpState == 0:
            if powerupID == 1:
                self.powerUpState = 1
                self.traits['goTrait'].updateAnimation(bigAnimation)
                self.rect = pygame.Rect(self.rect.x, self.rect.y-32, 32, 64)
                self.invincibilityFrames = 20
                # self.dashboard.drawText("INSULIN+++", self.rect.x + self.camera.x, self.rect.y, 8)
