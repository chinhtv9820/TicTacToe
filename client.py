import socket
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog

HOST = '127.0.0.1'
PORT = 55555

class TicTacToeClient:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Game Tic-Tac-Toe")
        
        self.client = None
        self.my_name = ""
        self.my_symbol = ""
        self.opponent_name = ""
        self.is_my_turn = False
        
        self.build_login_ui()
        self.window.mainloop()
        
    def build_login_ui(self):
        """Giao diện đăng nhập"""
        self.login_frame = tk.Frame(self.window)
        self.login_frame.pack(padx=20, pady=20)

        tk.Label(self.login_frame, text="Nhập tên của bạn:", font=("Arial", 12)).pack()
        self.name_entry = tk.Entry(self.login_frame, font=("Arial", 12))
        self.name_entry.pack(pady=5)
        
        tk.Button(self.login_frame, text="Tìm trận đấu", command=self.connect_to_server).pack(pady=10)
    
    def connect_to_server(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showwarning("Lỗi", "Vui lòng nhập tên!")
            return

        self.my_name = name
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((HOST, PORT))
            # Gửi gói tin LOGIN
            self.client.send(f"LOGIN {self.my_name}".encode('utf-8'))
            
            # Chuyển sang màn hình chờ/game
            self.login_frame.pack_forget()
            self.build_game_ui()
            
            # Bắt đầu lắng nghe
            threading.Thread(target=self.receive_message, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối Server: {e}")
            
    def build_game_ui(self):
        """Giao diện bàn cờ"""
        self.game_frame = tk.Frame(self.window)
        self.game_frame.pack()

        # Header hiển thị thông tin
        self.info_label = tk.Label(self.game_frame, text="Đang tìm đối thủ...", font=("Arial", 12, "bold"))
        self.info_label.pack(pady=10)

        # Bàn cờ
        self.board_frame = tk.Frame(self.game_frame)
        self.board_frame.pack()
        
        self.buttons = []
        for i in range(9):
            btn = tk.Button(self.board_frame, text="", font=("Arial", 24), width=5, height=2,
                            command=lambda idx=i: self.send_move(idx))
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)
        
        # Nút chơi lại (ẩn đi ban đầu)
        self.rematch_btn = tk.Button(self.game_frame, text="Chơi lại ván mới", state=tk.DISABLED, 
                                     command=self.send_rematch, bg="lightblue")
        self.rematch_btn.pack(pady=10)

    def send_move(self, index):
        if self.is_my_turn and self.buttons[index]['text'] == "":
            self.client.send(f"MOVE {index}".encode('utf-8'))

    def send_rematch(self):
        self.client.send("REMATCH".encode('utf-8'))
        self.rematch_btn.config(text="Đã gửi yêu cầu...", state=tk.DISABLED)

    def reset_board(self):
        for btn in self.buttons:
            btn.config(text="", bg="SystemButtonFace")
        self.rematch_btn.config(text="Chơi lại ván mới", state=tk.DISABLED)

    def receive_message(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if not message: break
                
                parts = message.split(" ", 2) # Tách tối đa 3 phần
                cmd = parts[0]
