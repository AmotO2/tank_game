import pygame

class Renderer:
    def __init__ (self):
        pass
    
    def set_fps(self, fps:int = 60):
        clock = pygame.time.Clock()
        clock.tick(fps)
    