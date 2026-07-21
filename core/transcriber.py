import whisper
from config import WHISPER_MODEL


class Transcriber:

    def __init__(self):
        print("Loading Whisper model...")
        self.model = whisper.load_model(WHISPER_MODEL)

    def transcribe(self, audio_path: str):

        result = self.model.transcribe(
            audio_path,
            fp16=False
        )

        transcript = result["text"]

        language = result["language"]

        segments = []

        for segment in result["segments"]:

            segments.append({
                "start": round(segment["start"], 2),
                "end": round(segment["end"], 2),
                "text": segment["text"].strip()
            })

        return {
            "language": language,
            "transcript": transcript,
            "segments": segments
        }