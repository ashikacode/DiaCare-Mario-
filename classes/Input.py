import pygame
from pygame.locals import *
import sys
import hid

class Input:
    
    def __init__(self, entity,dashboard,screen):
        self.mouseX = 0
        self.mouseY = 0
        self.entity = entity
        self.dashboard = dashboard  # Add this line
        self.screen = screen  # Store the screen as an attribute
        self.popup_image = None  # Store the current popup image
        self.popup_visible = False  # Track whether the popup is visible

    def find_joystick(self):
            devices = hid.enumerate()
            for device in devices:
                # Add your joystick's Vendor ID and Product ID
                if device['vendor_id'] == 0x081f and device['product_id'] == 0xe401:
                    return device
            return None
        
    def read_joystick_input(self, device_info):
        if device_info:
            device = hid.device()
            device.open(device_info['vendor_id'], device_info['product_id'])
            print(f"Connected to {device_info['product_string']}")

            try:
                #while True:
                data = device.read(64)  # Read 64 bytes from the device
                if data:
                    self.process_joystick_data(data)
            except KeyboardInterrupt:
                print("\nExiting...")
            finally:
                device.close()
        else:
            print("Joystick not found.")

    def process_joystick_data(self, data):
        # Example data processing
        # The actual format depends on your joystick. Here, we assume:
        # data[0] contains button states (each bit represents a button)
        # data[1] and data[2] contain X and Y axis values

        # For illustration, we assume:
        # Button 1 is represented by bit 0 of data[0]
        # Button 2 is represented by bit 1 of data[0]

        left_pressed = data[0] == 0;#data == [255, 0, 128, 128, 128, 15, 0, 0]#data[0] & 0x01
        right_pressed = data[0] == 255 #data == [0, 0, 128, 128, 128, 15, 0, 0]#data[0] & 0x02

        up_pressed = data[1] == 0;
        down_pressed = data[1] == 255;

        if left_pressed:
            self.perform_action_for_left()
            print("left")

        elif right_pressed:
            self.perform_action_for_right()

        elif down_pressed:
            self.perform_action_for_down()

        else:
            self.entity.traits['goTrait'].direction = 0

        if up_pressed:
            self.perform_action_for_up()
        
        else:
            self.entity.traits['jumpTrait'].jump(False)

    def perform_action_for_left(self):
        print("Action for Left")
        self.entity.traits["goTrait"].direction = -1

    def perform_action_for_right(self):
        print("Action for Right")
        self.entity.traits["goTrait"].direction = 1

    def perform_action_for_up(self):
        print("Action for Up")
        self.entity.traits['jumpTrait'].jump(True)

    def perform_action_for_down(self):
        print("Action for Down")


    def checkForInput(self):
        events = pygame.event.get()
        #self.checkForKeyboardInput()
        self.checkForJoyStickInput()
        self.checkForMouseInput(events)
        self.checkForQuitAndRestartInputEvents(events)
        if self.popup_visible:  # Check if the popup should be drawn
            self.drawPopup()

    def checkForKeyboardInput(self):
        pressedKeys = pygame.key.get_pressed()

        if pressedKeys[K_LEFT] or pressedKeys[K_h] and not pressedKeys[K_RIGHT]:
            self.entity.traits["goTrait"].direction = -1
        elif pressedKeys[K_RIGHT] or pressedKeys[K_l] and not pressedKeys[K_LEFT]:
            self.entity.traits["goTrait"].direction = 1
        else:
            self.entity.traits['goTrait'].direction = 0

        isJumping = pressedKeys[K_SPACE] or pressedKeys[K_UP] or pressedKeys[K_k]
        self.entity.traits['jumpTrait'].jump(isJumping)

        self.entity.traits['goTrait'].boost = pressedKeys[K_LSHIFT]

    def checkForJoyStickInput(self):
        joystick_info = self.find_joystick()
        self.read_joystick_input(joystick_info);
    
    # def showPopup(self, image_file):
    #     image = pygame.image.load(image_file)
    #     self.screen.blit(image, (100, 100))  # Example position and size
    #     pygame.display.update()

    # def showPopup(self, image_file):
    #         self.popup_image = pygame.image.load(image_file)
    #         self.popup_visible = True  # Set the popup as visible
    
    def showPopup(self, image_file):
        # Load the original image
        original_image = pygame.image.load(image_file)

        # Specify new dimensions
        new_width = 300  # Set the width you want
        new_height = 250  # Set the height you want

        # Scale the image to the new dimensions
        scaled_image = pygame.transform.scale(original_image, (new_width, new_height))

        # Store the scaled image and mark the popup as visible
        self.popup_image = scaled_image
        self.popup_visible = True


    def drawPopup(self):
        if self.popup_visible and self.popup_image:
            # Calculate the center of the screen to display the popup
            rect = self.popup_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(self.popup_image, rect)
            pygame.display.update()

    def checkForMouseInput(self, events):
        mouseX, mouseY = pygame.mouse.get_pos()

        # Check for mouse clicks to handle popup interaction
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = (mouseX, mouseY)

                # If there's a popup visible, dismiss it when clicking outside its area
                if self.popup_visible:
                    if not self.popup_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2)).collidepoint(pos):
                        self.popup_visible = False  # Hide the popup if clicked outside
                    continue  # Skip further processing to stop spawning objects while popup is active

                # Check for text element clicks
                if self.dashboard.glucose_text_rect.collidepoint(pos):
                    self.showPopup('./img/Glucose Bar.png')
                    return  # Stop further processing to avoid triggering other actions
                elif self.dashboard.insulin_text_rect.collidepoint(pos):
                    self.showPopup('./img/Insulin bar.png')
                    return  # Stop further processing to avoid triggering other actions
                # elif self.dashboard.glucagon_text_rect.collidepoint(pos):
                #     self.showPopup('./img/glucagon.png')
                #     return  # Stop further processing to avoid triggering other actions

        # Only add objects if no popup is active
        # if not self.popup_visible:
        #     if self.isRightMouseButtonPressed(events):
        #         self.entity.levelObj.addKoopa(
        #             mouseY / 32, mouseX / 32 - self.entity.camera.pos.x
        #         )
        #         self.entity.levelObj.addGoomba(
        #             mouseY / 32, mouseX / 32 - self.entity.camera.pos.x
        #         )
        #         self.entity.levelObj.addRedMushroom(
        #             mouseY / 32, mouseX / 32 - self.entity.camera.pos.x
        #         )
        #     if self.isLeftMouseButtonPressed(events):
        #         self.entity.levelObj.addCoin(
        #             mouseX / 32 - self.entity.camera.pos.x, mouseY / 32
        #         )



    def checkForQuitAndRestartInputEvents(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and \
                (event.key == pygame.K_ESCAPE or event.key == pygame.K_F5):
                self.entity.pause = True
                self.entity.pauseObj.createBackgroundBlur()

    def isLeftMouseButtonPressed(self, events):
        return self.checkMouse(events, 1)

    def isRightMouseButtonPressed(self, events):
        return self.checkMouse(events, 3)

    def checkMouse(self, events, button):
        for e in events:
            if e.type == pygame.MOUSEBUTTONUP and e.button == button:
                return True
        return False
