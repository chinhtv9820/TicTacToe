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
