import pygame

class Screen:
    def __init__(self, width:int = 1000, height:int = 700, caption:str = "Tank_Game"):
        self.width = width
        self.height = height
        self.WINDOW = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
    
    def set_bg_color(self,color:tuple = (255, 255, 255)):
        self.WINDOW.fill(color)
    
    def get_WINDOW(self):
        return self.WINDOW
        
    def load_image(self, image_path:str):
        image = pygame.image.load(image_path)
        return image
    
    def draw_image(self,image, location:tuple):
        self.WINDOW.blit(image, location)
    
    def resize_image(self, image, size:tuple):
        resized_image = pygame.transform.scale(image, size)
        return resized_image
        
    def update_display(self):
        pygame.display.update()
        
    def get_x_y_position(self, width, height, width_size, height_size):
        return pygame.Rect(width, height, width_size, height_size)
    
    def make_border_shape(self, width = 1000/2, x = 0, y = 10, height = 700):
        border = pygame.Rect(width, x, y, height)
        return border
    
    def draw_rect(self, win, image, color = (0,0,0)):
        pygame.draw.rect(win, color, image)
    
    def set_fps(self, fps:int = 60):
        clock = pygame.time.Clock()
        clock.tick(fps)
        
    def check_close_window(self, close:bool):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = True
        pygame.quit
        return close
        