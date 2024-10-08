from screen import Screen
from tank import Tank
from map import Map
import socket
import threading
import pygame
import time
import pickle

class Movement(Tank):
    def __init__(self, velocity:int = 5):
        self.VELOCITY = velocity
        self.shot = False
        self.current_turn = None
    
    def switch_turn(self, current_turn):
        """Switch turns between player1 and player2."""
        if current_turn == 'player1':
            current_turn = 'player2'
            print(f"Now it's {current_turn}'s turn.")
            return current_turn
        else:
            current_turn = 'player1'
            print(f"Now it's {current_turn}'s turn.")
            return current_turn
        
    def movement_keys(self,key, current_turn, image_pos:pygame.Rect, tank, border:pygame.Rect, side:int = 1):
        if key == 'A':
            if side == 1 and image_pos.x - self.VELOCITY > border.x + 10:    #left
                image_pos.x -= self.VELOCITY
            elif side == -1 and image_pos.x - self.VELOCITY > 20:
                image_pos.x -= self.VELOCITY
                
        if key == 'D':
            if side == 1 and image_pos.x + self.VELOCITY < 900:    #right
                image_pos.x += self.VELOCITY
            elif side == -1 and image_pos.x + self.VELOCITY < border.x - 80:
                image_pos.x += self.VELOCITY
                
        if key == 'Space' and len(tank.bullets) < 1:   
            tank.shoot(10)
            for bullet in tank.bullets:
                if bullet.active == True:
                    self.current_turn = self.switch_turn(current_turn)
                    time.sleep(0.5)
    
    @property
    def shot(self):
        return self._shot
    @shot.setter
    def shot(self, new_shot):
        self._shot = new_shot

class Game_managment:
    def __init__ (self, host = '127.0.0.1', port = 55555):
        self.server_host = host
        self.server_port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer_size = 1024
        self.players = {}  # Dictionary to store player info {player_name: addr}
        self.current_turn = 'player1'  # Start with player1's turn
        self.end = False
        self.SCREEN = Screen()
        self.MAP = Map
        self.turn = False
        self.bullets = []
        self.tanks = []
        self.MOVEMENT = Movement(1)
        self.blue_pos = None
        self.red_pos = None
        self.blue_tank = Tank("player1", 20, 50, 80, 60, 800, 500, 'blue_final.png', self.blue_pos)
        self.red_tank = Tank("player2", 20, 50, 80, 60, 100, 500, 'red_final.png', self.red_pos)
        self.tanks.append(self.blue_tank)
        self.tanks.append(self.red_tank)
        self.BORDER = self.SCREEN.make_border_shape()
        
        
    def draw_window(self, blue_pos, red_pos):
        self.red_tank.x = red_pos.x + 80
        self.red_tank.y = red_pos.y
        self.blue_tank.x = blue_pos.x
        self.blue_tank.y = blue_pos.y
        self.SCREEN.set_bg_color()
        self.MAP.Central_hill(self.SCREEN.WINDOW)
        self.SCREEN.draw_image(self.blue_tank.tank_image, (blue_pos.x, blue_pos.y))
        self.SCREEN.draw_image(self.red_tank.tank_image, (red_pos.x, red_pos.y))
        self.SCREEN.draw_rect(self.SCREEN.get_WINDOW(), self.SCREEN.make_border_shape())
        self.blue_tank.update_bullets()
        self.blue_tank.draw_bullet(self.SCREEN.get_WINDOW())
        self.red_tank.update_bullets()
        self.red_tank.draw_bullet(self.SCREEN.get_WINDOW())
        self.SCREEN.update_display()
        
    def handle_client(self, client_socket, addr):
        while True:
            try:
                data = client_socket.recv(self.buffer_size)
                if not data:
                    break
                #add end condition here
                
                # Deserialize the data
                data = pickle.loads(data)
                player = data.get('player')
                key = data.get('key')

                # Register player if not already registered
                if player not in self.players:
                    self.players[player] = addr
                    print(f"Registered {player} from {addr}")

                # Process input only if it's the player's turn
                if player == self.current_turn:
                    if player and key:
                        print(f"{player} pressed {key}")
                        if player == 'player1':
                            self.MOVEMENT.movement_keys(key, self.current_turn, self.blue_pos, self.blue_tank, self.BORDER)
                            self.current_turn = self.MOVEMENT.current_turn
                        else:
                            self.MOVEMENT.movement_keys(key, self.current_turn, self.red_pos, self.red_tank, self.BORDER, -1)
                            self.current_turn = self.MOVEMENT.current_turn

            except (EOFError, ConnectionResetError, pickle.UnpicklingError) as e:
                print(f"Connection error from {addr}: {e}")
                break
                #add end condition here
        client_socket.close()
        print(f"Connection from {addr} closed.")
    
    def start_server(self):
        self.server_socket.bind((self.server_host, self.server_port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.server_host}:{self.server_port}")
        
        while len(self.players) < 2:
            client_socket, addr = self.server_socket.accept()
            print(f"New connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()

    def shutdown_server(self):
        self.server_socket.close()
        print("Server shutdown.")


    def run(self):
        self.blue_pos = self.SCREEN.get_x_y_position(self.blue_tank.x, self.blue_tank.y, self.blue_tank.width, self.blue_tank.height)
        self.red_pos = self.SCREEN.get_x_y_position(self.red_tank.x, self.red_tank.y, self.red_tank.width, self.red_tank.height)
        while not self.end:
            self.SCREEN.set_fps()
            self.end = self.SCREEN.check_close_window(self.end)
            self.draw_window(self.blue_pos, self.red_pos)
            
            
if __name__ == "__main__":
    gamemng = Game_managment()
    try:
        gamemng.start_server()
        gamemng.run()
    except KeyboardInterrupt:
        gamemng.shutdown_server()
    
            