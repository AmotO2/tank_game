from screen import Screen
from movement import Movement
from tank import Tank
from map import Map
import socket
import threading

class Game_managment:
    def __init__ (self, host = "127.0.0.1", port = 55555):
        self.end = False
        self.SCREEN = Screen()
        self.MAP = Map
        self.turn = False
        self.bullets = []
        self.MOVMENT = Movement(1)
        self.HOST = host
        self.PORT = port
        self.blue_tank = Tank("player1", 20, 50, 80, 60, 800, 500, 'blue_final.png')
        self.red_tank = Tank("player2", 20, 50, 80, 60, 100, 500, 'red_final.png')
        self.BORDER = self.SCREEN.make_border_shape()
        
        # Initialize socket outside the 'with' block to keep it open
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.HOST, self.PORT))
        self.socket.listen()
        print(f"Server listening on {self.HOST}:{self.PORT}")
        
    def handle_client(self, conn: socket.socket, addr: tuple) -> None:
        print(f"Connected by {addr}")
        with conn:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                message = data.decode('utf-8')
                if message.strip() == "\exit":
                    print(f"Connection with {addr} closed.")
                    break
                conn.sendall(data)
        conn.close()
        
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

    def run(self):
        blue_pos = self.SCREEN.get_x_y_position(self.blue_tank.x, self.blue_tank.y, self.blue_tank.width, self.blue_tank.height)
        red_pos = self.SCREEN.get_x_y_position(self.red_tank.x, self.red_tank.y, self.red_tank.width, self.red_tank.height)
        while not self.end:
            
            self.SCREEN.set_fps()
            self.end = self.SCREEN.check_close_window(self.end)
            self.draw_window(blue_pos, red_pos)
            conn, addr = self.socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            client_thread.start()
            if self.turn == False:
                self.MOVMENT.movement_keys(blue_pos, self.blue_tank, self.BORDER)
                self.turn = self.MOVMENT.shot
            else:
                self.MOVMENT.movement_keys(red_pos, self.red_tank, self.BORDER, -1)
                self.turn = self.MOVMENT.shot
            
if __name__ == "__main__":
    gamemng = Game_managment()
    gamemng.run()
            