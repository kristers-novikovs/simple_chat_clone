import customtkinter as ctk
import threading
import socket
from chat import ChatGUI


class LauncherGUI:
    def __init__(self, master):
        self.master = master
        self.setup_gui()

    def setup_gui(self):
        self.username_var = ctk.StringVar()
        self.username_var.set("user")  # Default username

        self.connection_type_var = ctk.StringVar()
        self.connection_type_var.set("server")

        self.ip_address_var = ctk.StringVar()
        self.ip_address_var.set("127.0.0.1")

        self.port_var = ctk.IntVar()
        self.port_var.set(12345)

        self.frame = ctk.CTkFrame(master=self.master)
        self.frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Title label
        title_label = ctk.CTkLabel(
            self.frame, text="Simple Chat Launcher", font=("Helvetica", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Username entry
        ctk.CTkLabel(self.frame, text="Username:").grid(
            row=1, column=0, sticky="w", padx=5
        )
        username_entry = ctk.CTkEntry(self.frame, textvariable=self.username_var)
        username_entry.grid(row=1, column=1, columnspan=2, sticky="w", padx=5)

        # Connection type radio buttons
        ctk.CTkLabel(self.frame, text="Connection Type:").grid(
            row=2, column=0, sticky="w", padx=5
        )
        server_radio = ctk.CTkRadioButton(
            self.frame, text="Server", variable=self.connection_type_var, value="server"
        )
        server_radio.grid(row=2, column=1, sticky="w", padx=5)
        client_radio = ctk.CTkRadioButton(
            self.frame, text="Client", variable=self.connection_type_var, value="client"
        )
        client_radio.grid(row=2, column=2, sticky="w", padx=5)

        # IP address entry
        ctk.CTkLabel(self.frame, text="IP Address:").grid(
            row=3, column=0, sticky="w", padx=5
        )
        ip_address_entry = ctk.CTkEntry(self.frame, textvariable=self.ip_address_var)
        ip_address_entry.grid(row=3, column=1, columnspan=2, sticky="w", padx=5)

        # Port entry
        ctk.CTkLabel(self.frame, text="Port:").grid(row=4, column=0, sticky="w", padx=5)
        port_entry = ctk.CTkEntry(self.frame, textvariable=self.port_var)
        port_entry.grid(row=4, column=1, columnspan=2, sticky="w", padx=5)

        # Connect button
        connect_button = ctk.CTkButton(self.frame, text="Connect", command=self.connect)
        connect_button.grid(row=5, column=1, columnspan=2, pady=10)

    def connect(self):
        # Get username, connection type, IP address, and port
        username = self.username_var.get()
        connection_type = self.connection_type_var.get()
        ip_address = self.ip_address_var.get()
        port = self.port_var.get()

        if connection_type == "server":
            threading.Thread(target=self.start_server, args=(ip_address, port)).start()
        else:
            threading.Thread(
                target=self.connect_to_server, args=(ip_address, port)
            ).start()

    def start_server(self, ip_address, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip_address, port))
        server.listen(1)
        print("Server started. Waiting for connections...")

        while True:
            client, addr = server.accept()
            print(f"Connection established with {addr}")
            threading.Thread(target=self.handle_client, args=(client,)).start()
            # Open chat window for server
            chat_root = ctk.CTk()
            chat_gui = ChatGUI(chat_root, "Server", ip_address, port, client)
            chat_root.mainloop()

    def handle_client(self, client):
        while True:
            data = client.recv(1024).decode("utf-8")
            if not data:
                break
            print(f"Received from client: {data}")
            # client.send("Message received by server".encode("utf-8"))  # Commented out automated response

        client.close()

    def connect_to_server(self, ip_address, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((ip_address, port))
            print("Connected to server.")
            # client.send("Hello from client".encode("utf-8"))  # Commented out automated message
            # response = client.recv(1024).decode("utf-8")
            # print(f"Server response: {response}")  # Commented out automated response

            # Launch ChatGUI here
            chat_root = ctk.CTk()
            chat_gui = ChatGUI(
                chat_root, self.username_var.get(), ip_address, port, client
            )
            chat_root.mainloop()
        except Exception as e:
            print(f"Error connecting to server: {e}")
        finally:
            client.close()
