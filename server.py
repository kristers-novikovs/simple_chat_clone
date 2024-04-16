import socket
import customtkinter as ctk
import threading
import tkinter as tk  # Import tkinter


class ConnectionDialog(tk.Toplevel):  # Use tk.Toplevel instead of customtkinter
    def __init__(self, master, addr):
        super().__init__(master)
        self.title("Connection")
        self.geometry("200x100")
        tk.Label(self, text=f"Connected to {addr}").pack(pady=20)
        tk.Button(self, text="OK", command=self.destroy).pack()


class LANChatServer:
    def __init__(self, master, ip_host, port):
        self.master = master
        self.ip_host = ip_host
        self.port = port
        self.client_sockets = []

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

        self.run_server()

    def run_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip_host, self.port))
        server.listen(5)

        while True:
            client, addr = server.accept()
            self.client_sockets.append(client)
            self.show_connection_dialog(addr)
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        while True:
            try:
                data = client.recv(1024).decode("utf-8")
                if not data:
                    break
                self.broadcast(data, client)
            except Exception as e:
                print(f"Error: {e}")
                break

        client.close()
        self.client_sockets.remove(client)

    def broadcast(self, message, sender):
        for client in self.client_sockets:
            if client != sender:
                try:
                    client.send(message.encode("utf-8"))
                except Exception as e:
                    print(f"Error broadcasting message: {e}")

    def show_connection_dialog(self, addr):
        dialog = ConnectionDialog(self.master, addr)
        self.master.wait_window(dialog)


if __name__ == "__main__":
    root = ctk.CTk()
    ip_host = "127.0.0.1"  # Change to the desired LAN IP of the server
    port = 12345  # Change to a desired port number
    LANChatServer(root, ip_host, port)
    root.mainloop()
