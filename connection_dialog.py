import tkinter as tk


class ConnectionDialog(tk.Toplevel):
    def __init__(self, parent, addr):
        super().__init__(parent)
        self.addr = addr

        self.title("Connection Info")
        self.geometry("300x100")

        tk.Label(self, text=f"Connected to {addr}").pack(pady=10)
