import os
import sys
import yt_dlp

def has_ytdlp() -> bool:
    """
    Check if yt-dlp library is available.
    """
    try:
        import yt_dlp
        return True
    except ImportError:
        return False

def get_video_info(url: str):
    """
    Fetch video info using yt_dlp library and return as dict.
    """
    ydl_opts = {
        'flat_playlist': True,
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            return ydl.extract_info(url, download=False)
        except Exception as e:
            raise Exception(f"Failed to fetch video info: {str(e)}")

def get_formats(url: str):
    """
    Returns a list of available formats for the given URL.
    """
    info = get_video_info(url)
    
    if info.get('_type') == 'playlist':
        # Generic options for playlists
        formats = [
            {'id': 'best', 'label': 'Best Quality', 'ext': 'mp4', 'resolution': 'best'},
            {'id': 'bestvideo+bestaudio/best', 'label': 'Best Video + Best Audio', 'ext': 'mkv/mp4', 'resolution': 'best'},
            {'id': 'worst', 'label': 'Worst Quality', 'ext': 'mp4', 'resolution': 'worst'},
            {'id': 'ba/b', 'label': 'Audio Only', 'ext': 'm4a/mp3', 'resolution': 'audio'}
        ]
        return formats, info.get('title', 'Playlist'), True

    if "formats" not in info:
        return [], info.get('title', 'Video'), False
    
    formats = []
    for f in info["formats"]:
        res = f.get('resolution') or f.get('format_note') or 'Unknown'
        ext = f.get('ext', 'unknown')
        f_id = f.get('format_id')
        filesize = f.get('filesize')
        
        size_str = f"{filesize / 1024 / 1024:.1f}MB" if filesize else "Unknown size"
        
        label = f"{res} ({ext}) - {size_str}"
        formats.append({
            'id': f_id,
            'label': label,
            'ext': ext,
            'resolution': res
        })
    return formats, info.get('title', 'Video'), False

def download_video(url: str, format_id: str, output_path: str = ".", is_playlist: bool = False) -> None:
    """
    Run yt_dlp to download the video or playlist.
    """
    os.makedirs(output_path, exist_ok=True)
    
    outtmpl = os.path.join(output_path, '%(title)s.%(ext)s')
    if is_playlist:
        outtmpl = os.path.join(output_path, '%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s')

    ydl_opts = {
        'format': format_id,
        'outtmpl': outtmpl,
        'noplaylist': not is_playlist,
    }
        
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        raise Exception(f"Download failed: {str(e)}")

def select_format(url: str) -> str:
    """
    CLI version of format selection.
    """
    try:
        formats, title = get_formats(url)
    except Exception as e:
        print(f"Error: {e}")
        return ""

    if not formats:
        print("No available options to download.")
        return ""

    print(f"Title: {title}")
    # List available formats.
    for i, fmt in enumerate(formats):
        print(f"{i} - {fmt['label']}")

    # Prompt user to select resolution.
    while True:
        choice = input("Select resolution by number [q to quit]: ")

        if choice == "q":
            return ""
        elif not choice.isdigit():
            print("Option must be a non-negative number. Please try again.")
            continue

        choice = int(choice)
        if choice >= len(formats):
            print("Invalid choice. Please try again.")
        else:
            return formats[choice]['id']

def confirm_download() -> bool:
    """
    Confirm download with user. Return True if confirmed, False otherwise.
    """
    while True:
        confirm = input("Download? [Y/n]: ")

        if confirm.lower() == 'n':
            return False
        elif confirm.lower() in ['y', '']:
            return True

def main():
    # Check for ytdlp installation.
    if not has_ytdlp():
        print("⚠️  yt-dlp is not installed.")
        sys.exit()

    # Prompt user for video URL.
    url = input("Enter video URL [q to exit]: ")

    if url.lower() == 'q':
        sys.exit()

    # List available download format for user to choose.
    format_id = select_format(url)

    # Confirm download and download video.
    if format_id != "":
        confirm = confirm_download()
        if not confirm:
            print("Download cancelled.")
        else:
            try:
                download_video(url, format_id)
                print("Download complete!")
            except Exception as e:
                print(f"Error: {e}")
    main()

if __name__ == "__main__":
    main()