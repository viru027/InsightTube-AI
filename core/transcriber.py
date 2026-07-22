import streamlit as st
import whisper

from config import WHISPER_MODEL


@st.cache_resource(show_spinner=False)
def load_whisper_model():
    """
    Load Whisper model only once during the lifetime
    of the Streamlit application.
    """
    print(f"Loading Whisper model: {WHISPER_MODEL}")
    return whisper.load_model(WHISPER_MODEL)


class Transcriber:

    def __init__(self):
        self.model = load_whisper_model()

    def transcribe(self, audio_path: str):

        result = self.model.transcribe(
            audio_path,
            fp16=False,
            verbose=False
        )

        transcript = result.get("text", "").strip()

        language = result.get("language", "unknown")

        segments = []

        for segment in result.get("segments", []):

            segments.append(
                {
                    "start": round(segment["start"], 2),
                    "end": round(segment["end"], 2),
                    "text": segment["text"].strip(),
                }
            )

        return {
            "language": language,
            "transcript": transcript,
            "segments": segments,
        }