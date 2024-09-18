import pygame
from tank import Tank
import time
import socket

class Movement(Tank):
    def __init__(self, velocity:int = 5):
        self.HOST = '127.0.0.1'
        self.PORT = 9673
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.HOST, self.PORT))
        self.VELOCITY = velocity
        self.shot = False
        
    def movement_keys(self, image_pos:pygame.Rect, tank:Tank, border:pygame.Rect, side:int = 1):
        while True:
            message = input("Enter message to send (type '\\exit' to quit): ")
            self.socket.sendall(message.encode('utf-8'))
            if message == "\\exit":
                break
            data = self.socket.recv(4096)
            print(f"Received echo: {data.decode('utf-8')}")  
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