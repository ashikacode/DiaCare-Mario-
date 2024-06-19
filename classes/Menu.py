import json
import sys
import os
import pygame

from classes.Spritesheet import Spritesheet


class Menu:
    def __init__(self, screen, dashboard, level, sound):
        self.screen = screen
        self.sound = sound

        self.popup_images = [
            pygame.image.load("img/blood sugar managment (Popup1).png").convert_alpha(),
            pygame.image.load("img/blood sugar managment (Popup2).png").convert_alpha(),
            pygame.image.load("img/blood sugar managment (Popup3).png").convert_alpha(),
            pygame.image.load("img/blood sugar managment (Popup4).png").convert_alpha()
        ]
        self.popup_index = 0
        self.showing_popups = False


        self.popup_images1 = [
            pygame.image.load("img/Learn Dc3.png").convert_alpha(),
            pygame.image.load("img/Learn Dc4.png").convert_alpha(),
            pygame.image.load("img/Learn Dc1.png").convert_alpha(),
            pygame.image.load("img/Learn Dc2.png").convert_alpha()
        ]
        self.popup_index1 = 0
        self.showing_popups1 = False


        self.start = False
        self.inSettings = False
        self.state = 0
        self.level = level
        self.music = True
        self.sfx = True
        self.currSelectedLevel = 1
        self.levelNames = []
        self.inChoosingLevel = False
        self.dashboard = dashboard
        self.levelCount = 0
        
        self.learn_image = pygame.image.load("./img/Learn Dc1.png").convert_alpha()
        self.learn_image_rect = self.learn_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        self.spritesheet = Spritesheet("./img/title_screen.png")
        self.menu_banner = self.spritesheet.image_at(
            0,
            60,
            2,
            colorkey=[255, 0, 220],
            ignoreTileSize=True,
            xTileSize=180,
            yTileSize=88,
        )

        original_image = pygame.image.load("./img/Title DiaCare (1).png")
        original_image.set_colorkey([255, 0, 220], pygame.RLEACCEL)
        self.menu_banner = pygame.transform.scale(original_image, (180*2,180)) 
        self.menu_dot = self.spritesheet.image_at(
            0, 150, 2, colorkey=[255, 0, 220], ignoreTileSize=True
        )
        self.menu_dot2 = self.spritesheet.image_at(
            20, 150, 2, colorkey=[255, 0, 220], ignoreTileSize=True
        )
        self.loadSettings("./settings.json")

    def update(self):
        self.checkInput()
        if self.showing_popups:
            self.displayPopup()
        elif self.showing_popups1:
            self.displayPopup1()
        else:

            if self.inChoosingLevel:
                return

            self.drawMenuBackground()
            self.dashboard.update()

            if not self.inSettings:
                self.drawMenu()
            else:
                self.drawSettings()

    def displayPopup(self):
        # Display the current popup image
        self.screen.fill((0, 0, 0))  # Clear the screen or fill it with a background
        current_image = self.popup_images[self.popup_index]
        current_image = pygame.transform.scale(current_image, (640, 480))
        image_rect = current_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(current_image, image_rect)
        pygame.display.update()

    def displayPopup1(self):
        # Display the current popup image
        self.screen.fill((0, 0, 0))  # Clear the screen or fill it with a background
        current_image = self.popup_images1[self.popup_index1]
        current_image = pygame.transform.scale(current_image, (640, 480))
        image_rect = current_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(current_image, image_rect)
        pygame.display.update()

    def drawDot(self):
        if self.state == 0:
            self.screen.blit(self.menu_dot, (145, 263))
            self.screen.blit(self.menu_dot2, (145, 303))
            self.screen.blit(self.menu_dot2, (145, 343))
            if not self.inSettings:
                self.screen.blit(self.menu_dot2, (145, 383))
        elif self.state == 1:
            self.screen.blit(self.menu_dot, (145, 303))
            self.screen.blit(self.menu_dot2, (145, 263))
            self.screen.blit(self.menu_dot2, (145, 343))
            if not self.inSettings:
                self.screen.blit(self.menu_dot2, (145, 383))
        elif self.state == 2:
            self.screen.blit(self.menu_dot, (145, 343))
            self.screen.blit(self.menu_dot2, (145, 263))
            self.screen.blit(self.menu_dot2, (145, 303))
            if not self.inSettings:
                self.screen.blit(self.menu_dot2, (145, 383))
        elif self.state == 3:
            if not self.inSettings:
                self.screen.blit(self.menu_dot, (145, 383))
            self.screen.blit(self.menu_dot2, (145, 263))
            self.screen.blit(self.menu_dot2, (145, 303))
            self.screen.blit(self.menu_dot2, (145, 343))

    def loadSettings(self, url):
        try:
            with open(url) as jsonData:
                data = json.load(jsonData)
                if data["sound"]:
                    self.music = True
                    self.sound.music_channel.play(self.sound.soundtrack, loops=-1)
                else:
                    self.music = False
                if data["sfx"]:
                    self.sfx = True
                    self.sound.allowSFX = True
                else:
                    self.sound.allowSFX = False
                    self.sfx = False
        except (IOError, OSError):
            self.music = False
            self.sound.allowSFX = False
            self.sfx = False
            self.saveSettings("./settings.json")

    def saveSettings(self, url):
        data = {"sound": self.music, "sfx": self.sfx}
        with open(url, "w") as outfile:
            json.dump(data, outfile)

    def drawMenu(self):
        self.drawDot()
        self.dashboard.drawText("LEARN", 180, 270, 24)
        self.dashboard.drawText("CHOOSE LEVEL", 180, 310, 24)
        self.dashboard.drawText("SETTINGS", 180, 350, 24)
        self.dashboard.drawText("EXIT", 180, 390, 24)

    def drawMenuBackground(self, withBanner=True):
        for y in range(0, 13):
            for x in range(0, 20):
                self.screen.blit(
                    self.level.sprites.spriteCollection.get("sky").image,
                    (x * 32, y * 32),
                )
        for y in range(13, 15):
            for x in range(0, 20):
                self.screen.blit(
                    self.level.sprites.spriteCollection.get("ground").image,
                    (x * 32, y * 32),
                )
        if withBanner:
            self.screen.blit(self.menu_banner, (150, 80))
        self.screen.blit(
            self.level.sprites.spriteCollection.get("mario_idle").image,
            (2 * 32, 12 * 32),
        )
        self.screen.blit(
            self.level.sprites.spriteCollection.get("bush_1").image, (13 * 32, 12 * 32)
        )
        self.screen.blit(
            self.level.sprites.spriteCollection.get("bush_2").image, (14 * 32, 12 * 32)
        )
        self.screen.blit(
            self.level.sprites.spriteCollection.get("bush_2").image, (15 * 32, 12 * 32)
        )
        self.screen.blit(
            self.level.sprites.spriteCollection.get("bush_2").image, (16 * 32, 12 * 32)
        )
        self.screen.blit(
            self.level.sprites.spriteCollection.get("bush_3").image, (17 * 32, 12 * 32)
        )
        self.screen.blit(pygame.transform.scale(pygame.image.load('./img/icons/Burger.png').convert_alpha(), (32*1.5, 32*1.5)), (17.5*32, 12*32-16))

        

    def drawSettings(self):
        self.drawDot()
        self.dashboard.drawText("MUSIC", 180, 270, 24)
        if self.music:
            self.dashboard.drawText("ON", 340, 270, 24)
        else:
            self.dashboard.drawText("OFF", 340, 270, 24)
        self.dashboard.drawText("SFX", 180, 310, 24)
        if self.sfx:
            self.dashboard.drawText("ON", 340, 310, 24)
        else:
            self.dashboard.drawText("OFF", 340, 310, 24)
        self.dashboard.drawText("BACK", 180, 350, 24)

    def chooseLevel(self):
        self.drawMenuBackground(False)
        self.inChoosingLevel = True
        self.levelNames = self.loadLevelNames()
        self.drawLevelChooser()

    def drawBorder(self, x, y, width, height, color, thickness):
        pygame.draw.rect(self.screen, color, (x, y, width, thickness))
        pygame.draw.rect(self.screen, color, (x, y+width, width, thickness))
        pygame.draw.rect(self.screen, color, (x, y, thickness, width))
        pygame.draw.rect(self.screen, color, (x+width, y, thickness, width+thickness))

    def drawLevelChooser(self):
        j = 0
        offset = 75
        textOffset = 90
        names=["BLOOD GLUCOSE MONITORING","PRE-DIABETIC","DIABETIC"]
        nin=0
        for i, levelName in enumerate(self.loadLevelNames()):
            if self.currSelectedLevel == i+1:
                color = (255, 255, 255)
            else:
                color = (150, 150, 150)
            if i < 3:
                if nin<=2:
                    if len(names[nin])<=8:
                        self.dashboard.drawText(names[nin], 175*i+textOffset, 120, 12)
                    elif len(names[nin])<=12:
                        self.dashboard.drawText(names[nin][0:4], 175*i+textOffset, 110, 12)
                        self.dashboard.drawText(names[nin][4:], 175*i+textOffset, 110+20, 12)
                    else:
                        self.dashboard.drawText(names[nin][0:5], 175*i+textOffset, 100, 12)
                        self.dashboard.drawText(names[nin][6:13], 175*i+textOffset, 100+20, 12)
                        self.dashboard.drawText(names[nin][14:], 175*i+textOffset, 100+20+20, 12)
                    self.drawBorder(175*i+offset, 55, 145, 75, color, 5)
                    if nin<2:
                        nin+=1
            else:
                if nin<=2:
                    self.dashboard.drawText(names[nin], 175*j+textOffset, 250, 12)
                    self.drawBorder(175*j+offset, 210, 125, 75, color, 5)
                    j += 1
                    if nin<2:
                        nin+=1

    def loadLevelNames(self):
        files = []
        res = []
        for r, d, f in os.walk("./levels"):
            for file in f:
                files.append(os.path.join(r, file))
        for f in files:
            res.append(os.path.split(f)[1].split(".")[0])
        self.levelCount = len(res)
        return res

    def checkInput(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Handle ESC to close the game or popups, or go back from settings or level choosing
                if event.key == pygame.K_ESCAPE:
                    if self.showing_popups:
                        self.showing_popups=False
                        self.chooseLevel()
                    elif self.showing_popups1:
                        self.showing_popups1 = False
                    elif self.inChoosingLevel or self.inSettings:
                        self.inChoosingLevel = self.inSettings = False
                        self.__init__(self.screen, self.dashboard, self.level, self.sound)
                    else:
                        pygame.quit()
                        sys.exit()

                # Manage navigation through popups
                if self.showing_popups1:
                    if event.key in (pygame.K_RIGHT, pygame.K_RETURN):
                        if self.popup_index1 < len(self.popup_images1) - 1:
                            self.popup_index1 += 1
                        else:
                            self.showing_popups1 = False
                            self.popup_index1 = 0
                    elif event.key == pygame.K_LEFT:
                        if self.popup_index1 > 0:
                            self.popup_index1 -= 1
                        else:
                            self.showing_popups1 = False
                    continue
                    

                if self.showing_popups:
                    if event.key in (pygame.K_RIGHT, pygame.K_RETURN):
                        if self.popup_index < len(self.popup_images) - 1:
                            self.popup_index += 1
                        else:
                            self.startGame()
                    elif event.key == pygame.K_LEFT:
                        if self.popup_index > 0:
                            self.popup_index -= 1
                        else:
                            self.showing_popups = False
                            self.chooseLevel()

                # Navigation in menu and levels
                if not self.showing_popups and not self.showing_popups1:
                    if event.key == pygame.K_UP or event.key == pygame.K_k:
                        if self.inChoosingLevel and self.currSelectedLevel > 3:
                            self.currSelectedLevel -= 3
                            self.drawLevelChooser()
                        elif self.state > 0:
                            self.state -= 1

                    elif event.key == pygame.K_DOWN or event.key == pygame.K_j:
                        if self.inChoosingLevel and self.currSelectedLevel + 3 <= self.levelCount:
                            self.currSelectedLevel += 3
                            self.drawLevelChooser()
                        elif self.state < 3:
                            self.state += 1

                    elif event.key == pygame.K_LEFT or event.key == pygame.K_h:
                        if self.currSelectedLevel > 1:
                            self.currSelectedLevel -= 1
                            self.drawLevelChooser()

                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_l:
                        if self.currSelectedLevel < self.levelCount:
                            self.currSelectedLevel += 1
                            self.drawLevelChooser()

                    elif event.key == pygame.K_RETURN:
                        if self.inChoosingLevel:
                            self.showing_popups = True
                        elif self.state == 0:
                            if self.inSettings == False:
                                self.showing_popups1 = True
                            
                        elif self.state == 1:
                            if self.inSettings == False:
                                self.chooseLevel()
                        elif self.state == 2:
                            if self.inSettings == False:
                                self.state = 0
                                self.inSettings = True
                                
                        elif self.state == 3:
                            if self.inSettings == False:
                                pygame.quit()
                                sys.exit()
                # Handle settings changes
                if self.inSettings:
                    self.handleSettingsChanges(event)

        pygame.display.update()

    def startGame(self):
        self.inChoosingLevel = False
        self.showing_popups = False
        self.dashboard.state = "start"
        self.dashboard.time = 0
        self.level.loadLevel(self.levelNames[self.currSelectedLevel-1])
        self.dashboard.levelName = self.levelNames[self.currSelectedLevel-1].split("Level")[1]
        self.start = True

    def handleSettingsChanges(self, event):
        if event.key == pygame.K_RETURN:
            if self.state == 0:
                self.music = not self.music
                if self.music:
                    self.sound.music_channel.play(self.sound.soundtrack, loops=-1)
                else:
                    self.sound.music_channel.stop()
            elif self.state == 1:
                self.sfx = not self.sfx
                self.sound.allowSFX = self.sfx
            self.saveSettings("./settings.json")
            if self.state == 2:
                self.inSettings = False

