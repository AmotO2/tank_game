import socket
import pickle
import pygame
from tank import Tank
from movement import Movement

class Client:
    def __init__(self, player_id):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1000, 700
        self.WINDOW = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tank Game - Player " + player_id)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        
        # Connect to the server
        self.server_ip = '127.0.0.1'
        self.server_port = 5555
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((self.server_ip, self.server_port))

        # Movement and game setup
        self.player_id = player_id
        self.MOVEMENT = Movement(velocity=5)
        self.blue_tank = Tank("blue", 20, 50, 80, 60, 800, 500, 'blue_final.png')
        self.red_tank = Tank("red", 20, 50, 80, 60, 100, 500, 'red_final.png')

        self.run_game = True

    def draw_window(self, blue_tank_data, red_tank_data):
        self.WINDOW.fill((255, 255, 255))  # White background

        # Draw tanks
        pygame.draw.rect(self.WINDOW, (0, 0, 255), pygame.Rect(blue_tank_data['x'], blue_tank_data['y'], 80, 60))  # Blue tank
        pygame.draw.rect(self.WINDOW, (255, 0, 0), pygame.Rect(red_tank_data['x'], red_tank_data['y'], 80, 60))  # Red tank

        # Draw bullets
        for bullet in blue_tank_data['bullets']:
            pygame.draw.rect(self.WINDOW, (0, 0, 255), pygame.Rect(bullet[0], bullet[1], 10, 5))
        for bullet in red_tank_data['bullets']:
            pygame.draw.rect(self.WINDOW, (255, 0, 0), pygame.Rect(bullet[0], bullet[1], 10, 5))

        pygame.display.update()

    def send_data(self, command):
        data = pickle.dumps(command)
        self.server_socket.sendall(data)

    def receive_data(self):
        try:
            data = self.server_socket.recv(4096)
            if not data:
                return None
            return pickle.loads(data)
        except Exception as e:
            print(f"Error receiving data: {e}")
            return None

    def run(self):
        while self.run_game:
            self.clock.tick(60)  # Limit to 60 FPS
            self.handle_events()

            # Get the current game state from the server
            game_state = self.receive_data()

            if game_state is None:
                print("Lost connection to the server")
                break

            # Render the updated game state
            self.draw_window(game_state['blue_tank'], game_state['red_tank'])

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run_game = False
                pygame.quit()

        # Send movement and shooting actions to the server
        keys_pressed = pygame.key.get_pressed()
        command = {
            'left': keys_pressed[pygame.K_a],
            'right': keys_pressed[pygame.K_d],
            'shoot': keys_pressed[pygame.K_SPACE]
        }
        self.send_data(command)

if __name__ == "__main__":
    player_id = input("Enter your player ID (player1 or player2): ")
    client = Client(player_id)
    client.run()
