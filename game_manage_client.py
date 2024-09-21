from screen import Screen
from movement import Movement
from tank import Tank
from map import Map
from bullet import Bullet
import pygame
import pickle
import socket

class GameManagement:
    def __init__(self, player_id, server_conn):
        self.end = False
        self.SCREEN = Screen()
        self.MAP = Map
        self.turn = False
        self.bullets = []
        self.MOVEMENT = Movement(1)
        self.server_conn = server_conn  # Connection to the server
        self.player_id = player_id  # Player ID (either 0 or 1)

        # Assign tanks based on the player ID
        if player_id == 0:
            self.my_tank = Tank("player1", 20, 50, 80, 60, 800, 500, 'blue_final.png')
            self.other_tank = Tank("player2", 20, 50, 80, 60, 100, 500, 'red_final.png')
        else:
            self.my_tank = Tank("player2", 20, 50, 80, 60, 100, 500, 'red_final.png')
            self.other_tank = Tank("player1", 20, 50, 80, 60, 800, 500, 'blue_final.png')

        self.BORDER = self.SCREEN.make_border_shape()

    def draw_window(self):
        self.SCREEN.set_bg_color()  # White background
        self.MAP.Central_hill(self.SCREEN.WINDOW)  # Load map

        # Draw my tank
        self.SCREEN.draw_image(self.my_tank.tank_image, (self.my_tank.x, self.my_tank.y))
        # Draw the opponent's tank
        self.SCREEN.draw_image(self.other_tank.tank_image, (self.other_tank.x, self.other_tank.y))

        # Draw the border
        self.SCREEN.draw_rect(self.SCREEN.get_WINDOW(), self.BORDER)

        # Draw bullets
        self.my_tank.update_bullets()
        self.my_tank.draw_bullet(self.SCREEN.get_WINDOW())
        self.other_tank.update_bullets()
        self.other_tank.draw_bullet(self.SCREEN.get_WINDOW())

        self.SCREEN.update_display()

    def handle_input(self, keys):
        move_data = {
            'x': self.my_tank.x,
            'y': self.my_tank.y,
            'bullet': None
        }

        # Handle movement and shooting input
        if keys[pygame.K_a]:
            self.my_tank.x -= self.MOVEMENT.VELOCITY
        if keys[pygame.K_d]:
            self.my_tank.x += self.MOVEMENT.VELOCITY
        if keys[pygame.K_SPACE]:
            self.my_tank.shoot(10)
            if len(self.my_tank.bullets) > 0:
                bullet = self.my_tank.bullets[-1]  # Get the latest bullet
                move_data['bullet'] = {'x': bullet.x, 'y': bullet.y}

        move_data['x'] = self.my_tank.x
        move_data['y'] = self.my_tank.y
        return move_data

    def run(self):
        clock = pygame.time.Clock()
        while not self.end:
            self.SCREEN.set_fps()  # Set FPS

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end = True

            keys = pygame.key.get_pressed()
            move_data = self.handle_input(keys)

            # Send player input to the server
            self.server_conn.send(pickle.dumps(move_data))

            # Receive updated game state from server
            game_state = pickle.loads(self.server_conn.recv(4096))
            self.update_game_state(game_state)

            # Draw the window
            self.draw_window()

            clock.tick(60)

    def update_game_state(self, game_state):
        # Update the positions and bullets of both tanks based on server data
        if self.player_id == 0:
            self.other_tank.x = game_state['tank2']['x']
            self.other_tank.y = game_state['tank2']['y']
            self.other_tank.bullets = [Bullet(b['x'], b['y'], 10) for b in game_state['tank2']['bullets']]
        else:
            self.other_tank.x = game_state['tank1']['x']
            self.other_tank.y = game_state['tank1']['y']
            self.other_tank.bullets = [Bullet(b['x'], b['y'], 10) for b in game_state['tank1']['bullets']]
