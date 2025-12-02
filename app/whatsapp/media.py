from twilio.rest import Client
import httpx
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class MediaDownloader:
    """Download media from Twilio"""
    
    def __init__(self, account_sid: str, auth_token: str):
        self.account_sid = account_sid
        self.auth_token = auth_token
    
    async def download_media(self, media_url: str) -> bytes:
        """
        Download media file from Twilio
        
        Args:
            media_url: URL of the media file
            
        Returns:
            Media file bytes
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    media_url,
                    auth=(self.account_sid, self.auth_token),
                    timeout=30.0
                )
                response.raise_for_status()
                return response.content
        except Exception as e:
            logger.error(f"Failed to download media: {str(e)}")
            raise
    
    async def get_media_content_type(self, media_url: str) -> str:
        """
        Get content type of media file
        
        Args:
            media_url: URL of the media file
            
        Returns:
            Content type
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.head(
                    media_url,
                    auth=(self.account_sid, self.auth_token),
                    timeout=10.0
                )
                return response.headers.get("Content-Type", "")
        except Exception as e:
            logger.error(f"Failed to get media content type: {str(e)}")
            return ""
