from pathlib import Path
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi


class VideoExtractor:

    def __init__(self, download_dir="temp"):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------
    # Get YouTube Video Information
    # --------------------------------------------------------

    def get_info(self, url: str) -> dict:

        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "noplaylist": True,
            "extract_flat": False,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

            return {
                "id": info.get("id"),
                "title": info.get("title"),
                "channel": info.get("uploader"),
                "duration": info.get("duration"),
                "thumbnail": info.get("thumbnail"),
                "view_count": info.get("view_count"),
                "upload_date": info.get("upload_date"),
            }

        except Exception as e:
            raise Exception(f"Unable to fetch video information.\n\n{e}")

    # --------------------------------------------------------
    # Try Official YouTube Transcript
    # --------------------------------------------------------

    def get_transcript(self, video_id):

        try:

            api = YouTubeTranscriptApi()

            transcript = api.fetch(video_id)

            text = " ".join(snippet.text for snippet in transcript)

            segments = []

            for snippet in transcript:
                segments.append({
                    "start": snippet.start,
                    "end": snippet.start + snippet.duration,
                    "text": snippet.text,
                })

            return {
                "transcript": text,
                "segments": segments,
                "language": transcript.language,
            }

        except Exception as e:

            print("Transcript Error:", e)

            return None

    # --------------------------------------------------------
    # Download Audio (Whisper Fallback)
    # --------------------------------------------------------

    def download_audio(self, url: str) -> str:

        output_template = str(
            self.download_dir / "%(id)s.%(ext)s"
        )

        ydl_opts = {

            "format": "bestaudio/best",

            "outtmpl": output_template,

            "quiet": True,

            "noplaylist": True,

            "geo_bypass": True,

            "nocheckcertificate": True,

            "extract_flat": False,

            "postprocessors": [

                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }

            ],
        }

        try:

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:

                info = ydl.extract_info(
                    url,
                    download=True
                )

            audio_path = self.download_dir / f"{info['id']}.mp3"

            if not audio_path.exists():
                raise Exception(
                    "Audio file was not created."
                )

            return str(audio_path)

        except yt_dlp.utils.DownloadError:

            raise Exception(
                "❌ YouTube blocked the download (HTTP 403).\n\n"
                "Try another public video or one that has captions."
            )

        except Exception as e:

            raise Exception(
                f"Audio download failed.\n\n{e}"
            )

    # --------------------------------------------------------
    # Complete Processing Pipeline
    # --------------------------------------------------------

    def process(self, url: str):

        video = self.get_info(url)

        transcript_data = self.get_transcript(
            video["id"]
        )

        if transcript_data:

            return {
                "video": video,
                "transcript": transcript_data,
                "audio_path": None,
                "used_whisper": False,
            }

        audio_path = self.download_audio(url)

        return {
            "video": video,
            "audio_path": audio_path,
            "transcript": None,
            "used_whisper": True,
        }