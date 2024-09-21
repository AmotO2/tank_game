import socket
import threading
import pickle

class GameServer:
    def __init__(self, ip='0.0.0.0', port=55555):
        self.server_ip = ip
        self.server_port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer_size = 1024
        self.players = {}  # Dictionary to store player info {player_name: addr}
        self.current_turn = 'player1'  # Start with player1's turn

    def start_server(self):
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen(5)
        print(f"Server started and listening on {self.server_ip}:{self.server_port}")

        while len(self.players) < 2:
            client_socket, addr = self.server_socket.accept()
            print(f"New connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()

    def handle_client(self, client_socket, addr):
        while True:
            try:
                data = client_socket.recv(self.buffer_size)
                if not data:
                    break

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
                        # Switch turn after action
                        self.switch_turn()

            except (EOFError, ConnectionResetError, pickle.UnpicklingError) as e:
                print(f"Connection error from {addr}: {e}")
                break

        client_socket.close()
        print(f"Connection from {addr} closed.")

    def switch_turn(self):
        """Switch turns between player1 and player2."""
        if self.current_turn == 'player1':
            self.current_turn = 'player2'
        else:
            self.current_turn = 'player1'
        print(f"Now it's {self.current_turn}'s turn.")

    def shutdown_server(self):
        self.server_socket.close()
        print("Server shutdown.")


if __name__ == "__main__":
    server = GameServer()
    try:
        server.start_server()
    except KeyboardInterrupt:
        server.shutdown_server()
