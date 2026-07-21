from pathlib import Path
import yt_dlp


class VideoExtractor:
    def __init__(self, download_dir="temp"):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True)

    def get_info(self, url: str) -> dict:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return {
            "id": info["id"],
            "title": info["title"],
            "channel": info.get("uploader"),
            "duration": info.get("duration"),
            "thumbnail": info.get("thumbnail"),
            "view_count": info.get("view_count"),
            "upload_date": info.get("upload_date"),
        }

    def download_audio(self, url: str) -> str:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": str(self.download_dir / "%(id)s.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "noplaylist": True,
            "quiet": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        return str(self.download_dir / f"{info['id']}.mp3")

    def process(self, url: str) -> dict:
        return {
            "video": self.get_info(url),
            "audio_path": self.download_audio(url),
        }