import socket
import threading

HOST = '127.0.0.1'
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Server đang chạy tại {HOST}:{PORT}...")

class GameSession:
    def __init__(self, p1_socket, p2_socket, p1_name, p2_name):
        self.p1 = p1_socket
        self.p2 = p2_socket
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.board = [""] * 9
        self.turn = "X"
        self.rematch_state = {p1_socket: False, p2_socket: False}
        self.lock = threading.Lock()
