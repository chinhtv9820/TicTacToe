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

    def broadcast(self, message):
        """Gửi tin nhắn cho cả 2 client"""
        try:
            self.p1.send(message.encode('utf-8'))
            self.p2.send(message.encode('utf-8'))
        except:
            pass
            
    def send_to(self, socket, message):
        try:
            socket.send(message.encode('utf-8'))
        except:
            pass

    def reset_game(self):
        self.board = [""] * 9
        self.turn = "X"
        self.rematch_state = {self.p1: False, self.p2: False}
        self.broadcast("RESET")
        self.send_to(self.p1, "YOURTURN") # X đi trước

    def check_winner(self):
        wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for a, b, c in wins:
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] != "":
                return self.board[a] # Trả về X hoặc O
        if "" not in self.board:
            return "DRAW"
        return None

    def handle_move(self, sender_socket, index):
        with self.lock:
            # Xác định ai là người gửi
            symbol = "X" if sender_socket == self.p1 else "O"
            
            # Security: Kiểm tra đúng lượt và ô trống
            if symbol != self.turn or self.board[index] != "":
                return 

            # Cập nhật bàn cờ
            self.board[index] = symbol
            
            # Gửi cập nhật cho cả 2 bên
            self.broadcast(f"MOVE {index} {symbol}")

            # Kiểm tra thắng thua
            winner = self.check_winner()
            if winner:
                if winner == "DRAW":
                    self.broadcast("GAME_OVER DRAW Nobody")
                else:
                    win_name = self.p1_name if winner == "X" else self.p2_name
                    self.broadcast(f"GAME_OVER WIN {win_name}")
            else:
                # Đổi lượt
                self.turn = "O" if self.turn == "X" else "X"
                next_player = self.p1 if self.turn == "X" else self.p2
                self.send_to(next_player, "YOURTURN")

    def handle_rematch(self, sender_socket):
        self.rematch_state[sender_socket] = True
        # Nếu cả 2 đều đồng ý chơi lại
        if all(self.rematch_state.values()):
            self.reset_game()

def client_handler(client, name):
    # Hàm này chỉ dùng để giữ kết nối ban đầu cho đến khi ghép cặp
    pass

clients_queue = [] # Hàng đợi chứa (socket, name)

def wait_for_clients():
    while True:
        client, addr = server.accept()
        try:
            # Bước 1: Yêu cầu đăng nhập ngay khi kết nối
            name = client.recv(1024).decode('utf-8')
            if name.startswith("LOGIN"):
                player_name = name.split(" ", 1)[1]
                print(f"{player_name} đã kết nối từ {addr}")
                clients_queue.append((client, player_name))

                # Nếu đủ 2 người thì bắt đầu Game Session
                if len(clients_queue) >= 2:
                    p1 = clients_queue.pop(0)
                    p2 = clients_queue.pop(0)
                    start_game_session(p1, p2)
        except:
            continue

def start_game_session(p1_tuple, p2_tuple):
    sock1, name1 = p1_tuple
    sock2, name2 = p2_tuple
    
    session = GameSession(sock1, sock2, name1, name2)

    # Gửi tin nhắn bắt đầu
    # Format: START <Role> <OpponentName>
    session.send_to(sock1, f"START X {name2}")
    session.send_to(sock2, f"START O {name1}")
    session.send_to(sock1, "YOURTURN")

    # Tạo luồng lắng nghe riêng cho từng client trong session này
    t1 = threading.Thread(target=listen_to_player, args=(session, sock1, sock2))
    t2 = threading.Thread(target=listen_to_player, args=(session, sock2, sock1))
    t1.start()
    t2.start()

def listen_to_player(session, current_sock, opponent_sock):
    while True:
        try:
            msg = current_sock.recv(1024).decode('utf-8')
            if not msg: break
            
            if msg.startswith("MOVE"):
                idx = int(msg.split()[1])
                session.handle_move(current_sock, idx)
            elif msg == "REMATCH":
                session.handle_rematch(current_sock)
                
        except:
            break
    
    # Xử lý ngắt kết nối (QUIT)
    session.send_to(opponent_sock, "QUIT")
    current_sock.close()
