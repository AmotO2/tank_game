import pygame
import socket
import pickle
import sys

class Client:
    def __init__(self):
        self.server_host = '127.0.0.1'  # The server IP address
        self.server_port = 55555  # The server port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Pygame Initialization
        pygame.init()
        self.screen = pygame.display.set_mode((100, 100))
        pygame.display.set_caption("Tank Game Client")

        # Choose a player name (either 'player1' or 'player2')
        self.player_name = self.choose_player_name()

    def choose_player_name(self):
        while True:
            name = input("Choose your player name ('player1' or 'player2'): ").strip().lower()
            if name in ["player1", "player2"]:
                return name
            else:
                print("Invalid name! Please choose either 'player1' or 'player2'.")

    def connect_to_server(self):
        try:
            self.client_socket.connect((self.server_host, self.server_port))
            print(f"Connected to server at {self.server_host}:{self.server_port}")
        except Exception as e:
            print(f"Error connecting to server: {e}")
            sys.exit()

    def send_key_press(self, key):
        """Send the pressed key to the server."""
        data = {'player': self.player_name, 'key': key}
        try:
            self.client_socket.sendall(pickle.dumps(data))
        except Exception as e:
            print(f"Error sending data: {e}")

    def run(self):
        self.connect_to_server()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Detect key press events (use KEYDOWN for single key press events)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        print(f"{self.player_name} pressed 'A'")
                        self.send_key_press('A')
                    elif event.key == pygame.K_d:
                        print(f"{self.player_name} pressed 'D'")
                        self.send_key_press('D')
                    elif event.key == pygame.K_SPACE:
                        print(f"{self.player_name} pressed 'Space'")
                        self.send_key_press('Space')

            # Update the display (you can customize what is drawn here)
            self.screen.fill((0, 0, 0))  # Black background
            pygame.display.flip()

        self.client_socket.close()
        pygame.quit()


if __name__ == "__main__":
    client = Client()
    client.run()
