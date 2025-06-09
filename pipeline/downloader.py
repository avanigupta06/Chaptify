import re
import subprocess
from pathlib import Path

def clean_url(url):
    return re.sub(r'[\?&].*$', '', url)

def download_audio(youtube_url, output_path):
    youtube_url = clean_url(youtube_url)

    Path(output_path).mkdir(parents=True, exist_ok=True)

    command = [
        "yt-dlp",
        youtube_url,
        "-x",
        "--audio-format", "mp3",
        "--audio-quality", "192K",
        "--output", f"{output_path}/%(id)s.%(ext)s",
        "--ffmpeg-location", "E:/ffmpeg/bin",  # your actual ffmpeg path
        "--no-overwrites",
        "--continue",
        "--progress",
        "-N", "5"
    ]

    try:
        subprocess.run(command, check=True)

        # Return the first .mp3 file found in the output directory
        for file in Path(output_path).glob("*.mp3"):
            return file

        raise FileNotFoundError("MP3 file not found after download.")

    except subprocess.CalledProcessError as e:
        print(f"Error during download: {e}")
        raise e
