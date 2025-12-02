from twilio.rest import Client
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class WhatsAppClient:
    """Twilio WhatsApp client for sending messages"""
    
    def __init__(self, account_sid: str, auth_token: str, whatsapp_number: str):
        self.client = Client(account_sid, auth_token)
        self.whatsapp_number = whatsapp_number
    
    async def send_text_message(self, to: str, body: str) -> dict:
        """
        Send text message via WhatsApp
        
        Args:
            to: Recipient phone number (with whatsapp: prefix)
            body: Message text
            
        Returns:
            Message details
        """
        try:
            if not to.startswith("whatsapp:"):
                to = f"whatsapp:{to}"
            
            message = self.client.messages.create(
                from_=self.whatsapp_number,
                body=body,
                to=to
            )
            
            logger.info(f"Text message sent to {to}: {message.sid}")
            return {
                "sid": message.sid,
                "status": message.status,
                "to": to
            }
        except Exception as e:
            logger.error(f"Failed to send text message: {str(e)}")
            raise
    
    async def send_voice_message(self, to: str, media_url: str) -> dict:
        """
        Send voice message via WhatsApp
        
        Args:
            to: Recipient phone number
            media_url: URL of the audio file
            
        Returns:
            Message details
        """
        try:
            if not to.startswith("whatsapp:"):
                to = f"whatsapp:{to}"
            
            message = self.client.messages.create(
                from_=self.whatsapp_number,
                media_url=[media_url],
                to=to
            )
            
            logger.info(f"Voice message sent to {to}: {message.sid}")
            return {
                "sid": message.sid,
                "status": message.status,
                "to": to
            }
        except Exception as e:
            logger.error(f"Failed to send voice message: {str(e)}")
            raise
    
    async def send_message_with_media(self, to: str, body: str, media_url: str) -> dict:
        """
        Send message with media attachment
        
        Args:
            to: Recipient phone number
            body: Message text
            media_url: URL of the media file
            
        Returns:
            Message details
        """
        try:
            if not to.startswith("whatsapp:"):
                to = f"whatsapp:{to}"
            
            message = self.client.messages.create(
                from_=self.whatsapp_number,
                body=body,
                media_url=[media_url],
                to=to
            )
            
            logger.info(f"Message with media sent to {to}: {message.sid}")
            return {
                "sid": message.sid,
                "status": message.status,
                "to": to
            }
        except Exception as e:
            logger.error(f"Failed to send message with media: {str(e)}")
            raise
