import pygame
from tank import Tank
import time

class Movement(Tank):
    def __init__(self, velocity:int = 5):
        self.VELOCITY = velocity
        self.shot = False
        
    def movement_keys(self, image_pos:pygame.Rect, tank:Tank, border:pygame.Rect, side:int = 1):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a]:
            if side == 1 and image_pos.x - self.VELOCITY > border.x + 10:    #left
                image_pos.x -= self.VELOCITY
            elif side == -1 and image_pos.x - self.VELOCITY > 20:
                image_pos.x -= self.VELOCITY
                
        if keys_pressed[pygame.K_d]:
            if side == 1 and image_pos.x + self.VELOCITY < 900:    #right
                image_pos.x += self.VELOCITY
            elif side == -1 and image_pos.x + self.VELOCITY < border.x - 80:
                image_pos.x += self.VELOCITY
                
        if keys_pressed[pygame.K_SPACE] and len(tank.bullets) < 1:
                tank.shoot(10)
                for bullet in tank.bullets:
                    if bullet.active == True:
                        if self.shot == False:
                            self.shot = True
                            time.sleep(0.5)
                        else:
                            self.shot = False
                            time.sleep(0.5)
    
    @property
    def shot(self):
        return self._shot
    @shot.setter
    def shot(self, new_shot):
        self._shot = new_shot