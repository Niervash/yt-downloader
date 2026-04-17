import tkinter as tk
from gui import YtDownloaderGui
import Youtube_downloader as yt
from tkinter import messagebox

def main():
    if not yt.has_ytdlp():
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", "yt-dlp is not installed. Please install it (e.g., 'pip install yt-dlp') to use this app.")
        root.destroy()
        return

    root = tk.Tk()
    app = YtDownloaderGui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
