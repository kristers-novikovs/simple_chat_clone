import socket
import customtkinter as ctk
import threading
import tkinter as tk
from connection_dialog import ConnectionDialog  # Import ConnectionDialog
from chat import ChatGUI  # Import ChatGUI


class LANChatClient:
    def __init__(self, master, ip_host, port):
        self.master = master
        self.ip_host = ip_host
        self.port = port
        self.client_socket = None  # Initialize client_socket as None

        chat_frame = ctk.CTkFrame(self.master)
        chat_frame.pack(pady=20, padx=20, fill=ctk.BOTH, expand=True)

        self.chat_box = ctk.CTkTextbox(
            master=chat_frame,
            width=300,
            height=500,
            scrollbar_button_color="dark gray",
            corner_radius=16,
            border_color="black",
            border_width=2,
            state="normal",
        )
        self.chat_box.grid(
            row=0, column=0, padx=10, pady=10, columnspan=1, rowspan=10, sticky="nsew"
        )

        scrollbar_y = ctk.CTkScrollbar(
            master=chat_frame,
            orientation=ctk.VERTICAL,
            command=self.chat_box.yview,
        )
        scrollbar_y.grid(row=0, column=1, padx=(0, 10), pady=0, sticky="ns")

        self.chat_box.configure(yscrollcommand=scrollbar_y.set)

        self.run_client()

    def run_client(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.ip_host, self.port))
            print("Connected to server.")
            # Show connection dialog upon successful connection
            self.show_connection_dialog((self.ip_host, self.port))
            # Launch ChatGUI here
            chat_gui = ChatGUI(
                self.master, "Client", self.ip_host, self.port, self.client_socket
            )
            chat_gui.start_receiving()  # Start receiving messages
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def show_connection_dialog(self, addr):
        dialog = ConnectionDialog(self.master, addr)
        self.master.wait_window(dialog)


if __name__ == "__main__":
    root = ctk.CTk()
    ip_host = "127.0.0.1"  # Change to the server's LAN IP
    port = 12345  # Change to the server's port number
    LANChatClient(root, ip_host, port)
    root.mainloop()
