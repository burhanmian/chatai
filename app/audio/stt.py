import openai
from pathlib import Path
from typing import Optional


class WhisperSTT:
    """Speech-to-Text using OpenAI Whisper API"""
    
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
    
    async def transcribe(self, audio_path: str, language: str = "ur") -> str:
        """
        Transcribe audio file to text using Whisper API
        
        Args:
            audio_path: Path to audio file
            language: Language code (ur for Urdu, en for English)
            
        Returns:
            Transcribed text
        """
        try:
            with open(audio_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language
                )
            return transcript.text
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
    
    async def transcribe_auto_detect(self, audio_path: str) -> str:
        """
        Transcribe audio with automatic language detection
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Transcribed text
        """
        try:
            with open(audio_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return transcript.text
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
