import customtkinter as ctk
from src.gui import DownloaderApp

def main():
    root = ctk.CTk()
    app = DownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
