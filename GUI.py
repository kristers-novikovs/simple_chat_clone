import customtkinter as ctk
import threading


class ChatGUI:
    def __init__(self, master, username, ip_host, port, client_socket):
        self.master = master
        self.username = username
        self.ip_host = ip_host
        self.port = port
        self.client_socket = client_socket

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("user_themes/GreyGhost.json")

        self.master.resizable(False, False)
        self.master.geometry("800x600")
        self.master.title("LAN CHAT")
        self.master.iconbitmap("icon.ico")

        self.frame = ctk.CTkFrame(master=self.master)
        self.frame.pack(pady=20, padx=30, fill="both", expand=True)

        self.chat_box = ctk.CTkTextbox(
            master=self.frame,
            width=300,
            height=500,
            scrollbar_button_color="dark gray",
            corner_radius=16,
            border_color="black",
            border_width=2,
            state=ctk.DISABLED,
        )
        self.chat_box.grid(
            row=0, column=0, padx=10, pady=10, columnspan=1, rowspan=10, sticky="nsew"
        )

        self.scrollbar = ctk.CTkScrollbar(master=self.frame, orientation="vertical")
        self.scrollbar.grid(row=0, column=1, rowspan=10, sticky="ns")

        self.chat_box.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.chat_box.yview)

        self.message_entry = ctk.CTkEntry(
            master=self.frame, width=250, height=25, font=ctk.CTkFont(size=12)
        )
        self.message_entry.grid(
            row=11, column=0, pady=10, padx=10, columnspan=1, sticky="ew"
        )
        self.message_entry.bind("<Return>", lambda event: self.send_message())
        self.message_entry.bind("<Key>", lambda event: self.typing_indicator())

        self.send_button = ctk.CTkButton(
            master=self.frame,
            height=25,
            width=50,
            text="\u23CE",
            command=self.send_message,
        )
        self.send_button.grid(row=11, column=1, pady=10, padx=(0, 10), sticky="e")

        self.username_label = ctk.CTkLabel(
            master=self.frame, text=f"username: {self.username}"
        )
        self.username_label.grid(row=0, column=3, pady=10, padx=10, sticky="e")

        self.typing_indicator_label = ctk.CTkLabel(
            master=self.frame, text="", font=ctk.CTkFont(size=10), bg_color="#a9b8c4"
        )
        self.typing_indicator_label.grid(row=9, column=0, columnspan=2, padx=30, pady=0)

        self.typing = False

        # Receive messages in a separate thread
        threading.Thread(target=self.receive_messages).start()

    def send_message(self):
        message = self.message_entry.get()
        if message:
            formatted_message = f"{self.username}: {message}\n\n"
            self.chat_box.configure(state=ctk.NORMAL)
            self.chat_box.insert(ctk.END, formatted_message)
            self.chat_box.configure(state=ctk.DISABLED)
            self.message_entry.delete(0, ctk.END)
            self.typing_indicator_label.configure(text="")
            self.scroll_to_bottom()
            self.client_socket.send(formatted_message.encode())

    def typing_indicator(self):
        if not self.typing:
            self.typing_indicator_label.configure(text="Typing...")
            self.typing = True
        self.master.after(1000, self.reset_typing)

    def reset_typing(self):
        self.typing = False
        self.typing_indicator_label.configure(text="")

    def scroll_to_bottom(self):
        self.chat_box.yview_moveto(1.0)

    def receive_messages(self):
        while True:
            data = self.client_socket.recv(1024).decode("utf-8")
            if not data:
                break
            # Only display messages sent by other users
            if not data.startswith(self.username):
                self.master.after(0, self.display_received_message, data)

    def display_received_message(self, message):
        sender, received_message = message.split(": ", 1)
        formatted_message = f"{sender}: {received_message}\n"

        if sender == self.username:  # If the message was sent by the local user
            bg_color = "#c2f2c2"  # Light green background color for sender's messages
        else:
            bg_color = "#f0f0f0"  # Light gray background color for received messages

        self.chat_box.configure(state=ctk.NORMAL)
        self.chat_box.insert(ctk.END, formatted_message, "message")
        self.chat_box.tag_add("bg_color_tag", "message.first", "message.last")
        self.chat_box.tag_config("bg_color_tag", background=bg_color)
        self.chat_box.configure(state=ctk.DISABLED)
        self.scroll_to_bottom()
