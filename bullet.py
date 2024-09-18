import pygame
import time

class Bullet:
    def __init__(self, x, y, power, gravity=0.5, side = 1):
        self.x = x
        self.y = y
        self.vy = -power  # Initial upward velocity
        self.vx = side*10  # No horizontal velocity for now
        self.radius = 5
        self.color = (0, 0, 0)
        self.gravity = gravity
        self.active = True

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        if self.y > 600:
            self.active = False
            
    def check_active_bullet(self):
        if self.active == False:
            return self.active
        else:
            return True

    def draw(self, screen):
        if self.active:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        else:
            time.sleep(0.5)
            
    @property
    def active(self):
        return self._active
    @active.setter
    def active(self, new_active):
        self._active = new_active