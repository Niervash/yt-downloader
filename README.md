# YouTube Downloader GUI

A simple and efficient YouTube Video and Playlist downloader with a graphical user interface, powered by `yt-dlp`.

![YouTube Downloader](/assets/image.png)

## Features

- 📺 Download single videos or entire playlists.
- 🛠️ Select from multiple available resolutions and formats.
- 📂 Custom download directory selection.
- 🚀 Multi-threaded downloading (GUI remains responsive).
- 🎨 Modern Tkinter-based interface.

## Prerequisites

Before running the application, ensure you have Python installed. You also need `ffmpeg` installed on your system if you want to merge high-quality video and audio streams (optional but recommended).

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Niervash/yt-downloader.git
   cd "yt-downloader"
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application using:

```bash
python app.py
```

1. Paste the YouTube URL.
2. Click **Fetch Formats**.
3. Select your desired quality.
4. Choose the save location.
5. Click **Download**.

## Building for Windows (.exe)

To create a standalone `.exe` file for Windows:

1. Install PyInstaller:

   ```bash
   pip install pyinstaller
   ```

2. Run the build command:
   ```bash
   pyinstaller --noconfirm --onefile --windowed --add-data "assets;assets" --icon "assets/image.png" --name "YTDownloader" app.py
   ```

The executable will be generated in the `dist/` folder.

> **Note:** Since this app depends on `yt-dlp`, the simplest way to ensure it works on other machines is to make sure `yt-dlp` is bundled or the user has it. The current setup expects `yt-dlp` to be accessible.

## License

 Feel free to use and modify!
