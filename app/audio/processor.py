import aiofiles
import os
from pathlib import Path
from typing import Optional
from pydub import AudioSegment
import uuid


class AudioProcessor:
    """Process audio files for WhatsApp"""
    
    def __init__(self, cache_dir: str = "/tmp/audio_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    async def download_audio(self, url: str, file_id: Optional[str] = None) -> str:
        """
        Download audio file from URL
        
        Args:
            url: URL to download from
            file_id: Optional file ID, generates UUID if not provided
            
        Returns:
            Path to downloaded file
        """
        import httpx
        
        if not file_id:
            file_id = str(uuid.uuid4())
        
        file_path = self.cache_dir / f"{file_id}.ogg"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(response.content)
        
        return str(file_path)
    
    def convert_to_mp3(self, input_path: str, output_path: Optional[str] = None) -> str:
        """
        Convert audio file to MP3 format
        
        Args:
            input_path: Path to input audio file
            output_path: Optional output path
            
        Returns:
            Path to converted file
        """
        if not output_path:
            output_path = str(Path(input_path).with_suffix('.mp3'))
        
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format="mp3")
        
        return output_path
    
    def convert_to_ogg(self, input_path: str, output_path: Optional[str] = None) -> str:
        """
        Convert audio file to OGG format (WhatsApp compatible)
        
        Args:
            input_path: Path to input audio file
            output_path: Optional output path
            
        Returns:
            Path to converted file
        """
        if not output_path:
            output_path = str(Path(input_path).with_suffix('.ogg'))
        
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format="ogg", codec="libopus")
        
        return output_path
    
    async def save_audio(self, audio_bytes: bytes, file_id: Optional[str] = None, format: str = "mp3") -> str:
        """
        Save audio bytes to file
        
        Args:
            audio_bytes: Audio data
            file_id: Optional file ID
            format: Audio format (mp3, ogg, etc.)
            
        Returns:
            Path to saved file
        """
        if not file_id:
            file_id = str(uuid.uuid4())
        
        file_path = self.cache_dir / f"{file_id}.{format}"
        
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(audio_bytes)
        
        return str(file_path)
    
    def cleanup(self, file_path: str):
        """Delete audio file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass
