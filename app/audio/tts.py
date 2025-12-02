import httpx
from typing import Optional


class ElevenLabsTTS:
    """Text-to-Speech using ElevenLabs API"""
    
    def __init__(self, api_key: str, voice_id: str):
        self.api_key = api_key
        self.voice_id = voice_id
        self.base_url = "https://api.elevenlabs.io/v1"
    
    async def speak(self, text: str, model_id: str = "eleven_multilingual_v2") -> bytes:
        """
        Convert text to speech audio
        
        Args:
            text: Text to convert to speech
            model_id: ElevenLabs model ID
            
        Returns:
            Audio bytes
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/text-to-speech/{self.voice_id}",
                    headers={
                        "xi-api-key": self.api_key,
                        "Content-Type": "application/json"
                    },
                    json={
                        "text": text,
                        "model_id": model_id,
                        "voice_settings": {
                            "stability": 0.5,
                            "similarity_boost": 0.75
                        }
                    }
                )
                response.raise_for_status()
                return response.content
        except Exception as e:
            raise Exception(f"Text-to-speech failed: {str(e)}")
    
    async def speak_with_emotion(
        self, 
        text: str, 
        stability: float = 0.5, 
        similarity_boost: float = 0.75
    ) -> bytes:
        """
        Convert text to speech with custom emotion settings
        
        Args:
            text: Text to convert to speech
            stability: Voice stability (0-1)
            similarity_boost: Voice similarity boost (0-1)
            
        Returns:
            Audio bytes
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/text-to-speech/{self.voice_id}",
                    headers={
                        "xi-api-key": self.api_key,
                        "Content-Type": "application/json"
                    },
                    json={
                        "text": text,
                        "model_id": "eleven_multilingual_v2",
                        "voice_settings": {
                            "stability": stability,
                            "similarity_boost": similarity_boost
                        }
                    }
                )
                response.raise_for_status()
                return response.content
        except Exception as e:
            raise Exception(f"Text-to-speech failed: {str(e)}")
