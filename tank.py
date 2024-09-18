from screen import Screen
from bullet import Bullet

class Tank(Screen):
    def __init__(self, name:str, power:int, health:int, width:int, height:int, x:int, y:int, path:str):
        self.name = name
        self.power = power 
        self.health = health
        self.width = width
        self.height = height
        self.speed = 5
        self.bullets = []
        self.x = x
        self.y = y
        self.path = path
        self.tank_image = self.load_image(path)
        self.tank_image = self.resize_image(self.tank_image, (width, height))
            
    def shoot(self, power):
        side = 1
        if self.name == "player1":
            side = -1
        bullet = Bullet(self.x, self.y, power, side=side)
        self.bullets.append(bullet)

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.update()
        self.bullets = [bullet for bullet in self.bullets if bullet.active]
        

    def draw_bullet(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)
                 
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, new_name:str):
        self._name = new_name
        
    @property
    def power(self):
        return self._power
    @power.setter
    def power(self, new_power:int):
        self._power = new_power
    
    @property
    def health(self):
        return self._health
    @health.setter
    def health(self, new_health:int):
        self._health = new_health
    
    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, new_width:int):
        self._width = new_width
    
    @property
    def height(self):
        return self._height
    @height.setter
    def height(self, new_height:int):
        self._height = new_height
    
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, new_x:int):
        self._x = new_x
    
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, new_y:int):
        self._y = new_y
        
    @property
    def path(self):
        return self._path
    @path.setter
    def path(self, new_path:str):
        self._path = new_path
    
    @property
    def tank_image(self):
        return self._tank_image
    @tank_image.setter
    def tank_image(self, new_tank_image):
        self._tank_image = new_tank_image