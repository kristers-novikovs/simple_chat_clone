import customtkinter as ctk

from launcher_gui import LauncherGUI


def main():
    root = ctk.CTk()
    launcher_gui = LauncherGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
