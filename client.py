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
