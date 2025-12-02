import os
from typing import Optional


def get_audio_duration(file_path: str) -> float:
    """
    Get duration of audio file in seconds
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Duration in seconds
    """
    from pydub import AudioSegment
    
    audio = AudioSegment.from_file(file_path)
    return len(audio) / 1000.0


def get_audio_format(file_path: str) -> str:
    """
    Get audio format from file extension
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Audio format (mp3, ogg, etc.)
    """
    return os.path.splitext(file_path)[1][1:].lower()


def is_audio_file(file_path: str) -> bool:
    """
    Check if file is an audio file
    
    Args:
        file_path: Path to file
        
    Returns:
        True if audio file
    """
    audio_extensions = {'.mp3', '.ogg', '.wav', '.m4a', '.flac', '.aac'}
    ext = os.path.splitext(file_path)[1].lower()
    return ext in audio_extensions
