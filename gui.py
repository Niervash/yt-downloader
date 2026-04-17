import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import Youtube_downloader as yt
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class YtDownloaderGui:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("600x450")
        self.root.configure(bg="#f0f0f0")

        # Set Icon if available
        try:
            icon_path = resource_path('assets/file.png')
            if os.path.exists(icon_path):
                self.icon = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, self.icon)
        except Exception as e:
            print(f"Could not load icon: {e}")

        self.setup_ui()
        self.formats = []
        self.video_title = ""
        self.is_playlist = False

    def setup_ui(self):
        # Main Frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title Label
        title_label = ttk.Label(main_frame, text="YouTube Downloader", font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 20))

        # URL Input
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(url_frame, text="Video URL:").pack(side=tk.LEFT)
        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.url_entry.bind("<Return>", lambda e: self.fetch_info())

        self.fetch_btn = ttk.Button(main_frame, text="Fetch Formats", command=self.fetch_info)
        self.fetch_btn.pack(pady=10)

        # Info Display Area
        self.info_label = ttk.Label(main_frame, text="", wraplength=500, font=("Arial", 10, "italic"))
        self.info_label.pack(pady=5)

        # Format Selection
        format_frame = ttk.Frame(main_frame)
        format_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(format_frame, text="Select Format:").pack(side=tk.LEFT)
        self.format_combo = ttk.Combobox(format_frame, state="disabled", width=50)
        self.format_combo.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Download Path
        path_frame = ttk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(path_frame, text="Save to:").pack(side=tk.LEFT)
        self.path_entry = ttk.Entry(path_frame, width=40)
        self.path_entry.insert(0, os.path.expanduser("~/Downloads"))
        self.path_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(path_frame, text="Browse", command=self.browse_path).pack(side=tk.LEFT)

        # Download Button
        self.download_btn = ttk.Button(main_frame, text="Download Video", state="disabled", command=self.start_download)
        self.download_btn.pack(pady=20)

        # Progress/Status
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, font=("Arial", 9))
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def browse_path(self):
        directory = filedialog.askdirectory(initialdir=self.path_entry.get())
        if directory:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, directory)

    def fetch_info(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL")
            return

        self.fetch_btn.config(state="disabled")
        self.status_var.set("Fetching video information...")
        
        # Run in thread to not freeze GUI
        threading.Thread(target=self._fetch_info_thread, args=(url,), daemon=True).start()

    def _fetch_info_thread(self, url):
        try:
            formats, title, is_playlist = yt.get_formats(url)
            self.formats = formats
            self.video_title = title
            self.is_playlist = is_playlist
            
            # Update UI from thread
            self.root.after(0, self._on_info_fetched, title, is_playlist)
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.root.after(0, lambda: self.fetch_btn.config(state="normal"))

    def _on_info_fetched(self, title, is_playlist):
        prefix = "Playlist: " if is_playlist else "Video: "
        self.info_label.config(text=f"{prefix}{title}")
        
        btn_text = "Download Playlist" if is_playlist else "Download Video"
        self.download_btn.config(text=btn_text)

        format_labels = [f['label'] for f in self.formats]
        self.format_combo.config(values=format_labels, state="readonly")
        if format_labels:
            self.format_combo.current(0)
            self.download_btn.config(state="normal")
        
        self.fetch_btn.config(state="normal")
        self.status_var.set("Formats loaded.")

    def start_download(self):
        url = self.url_entry.get().strip()
        idx = self.format_combo.current()
        if idx < 0:
            return
            
        format_id = self.formats[idx]['id']
        save_path = self.path_entry.get().strip()
        
        self.download_btn.config(state="disabled")
        self.fetch_btn.config(state="disabled")
        self.status_var.set("Downloading... please wait.")
        
        threading.Thread(target=self._download_thread, args=(url, format_id, save_path, self.is_playlist), daemon=True).start()

    def _download_thread(self, url, format_id, save_path, is_playlist):
        try:
            yt.download_video(url, format_id, save_path, is_playlist)
            self.root.after(0, self._on_download_complete)
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Download failed: {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("Download Error", str(e)))
            self.root.after(0, self._enable_buttons)

    def _on_download_complete(self):
        self.status_var.set("Download complete!")
        messagebox.showinfo("Success", "Video downloaded successfully!")
        self._enable_buttons()

    def _enable_buttons(self):
        self.download_btn.config(state="normal")
        self.fetch_btn.config(state="normal")

if __name__ == "__main__":
    if not yt.has_ytdlp():
        # Simple message before starting tk
        print("yt-dlp not found. Please install it.")
        # We can still show a dialog
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", "yt-dlp is not installed. Please install it to use this app.")
        root.destroy()
    else:
        root = tk.Tk()
        app = YtDownloaderGui(root)
        root.mainloop()
