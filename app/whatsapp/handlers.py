from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class MessageHandler:
    """Handle incoming WhatsApp messages"""
    
    async def handle_text_message(self, message_data: Dict[str, Any]) -> str:
        """
        Handle incoming text message
        
        Args:
            message_data: Message data from Twilio webhook
            
        Returns:
            Extracted message text
        """
        body = message_data.get("Body", "")
        from_number = message_data.get("From", "")
        
        logger.info(f"Received text message from {from_number}: {body}")
        return body
    
    async def handle_voice_message(self, message_data: Dict[str, Any]) -> Optional[str]:
        """
        Handle incoming voice message
        
        Args:
            message_data: Message data from Twilio webhook
            
        Returns:
            Media URL if voice message exists
        """
        num_media = int(message_data.get("NumMedia", 0))
        
        if num_media > 0:
            media_url = message_data.get("MediaUrl0")
            media_type = message_data.get("MediaContentType0", "")
            from_number = message_data.get("From", "")
            
            if "audio" in media_type:
                logger.info(f"Received voice message from {from_number}: {media_url}")
                return media_url
        
        return None
    
    async def extract_sender_info(self, message_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Extract sender information from message
        
        Args:
            message_data: Message data from Twilio webhook
            
        Returns:
            Dictionary with sender info
        """
        from_number = message_data.get("From", "").replace("whatsapp:", "")
        profile_name = message_data.get("ProfileName", "")
        
        return {
            "phone_number": from_number,
            "name": profile_name
        }
    
    def parse_webhook_data(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse Twilio webhook form data
        
        Args:
            form_data: Raw form data from webhook
            
        Returns:
            Parsed message data
        """
        return {
            "From": form_data.get("From"),
            "To": form_data.get("To"),
            "Body": form_data.get("Body", ""),
            "NumMedia": form_data.get("NumMedia", 0),
            "MediaUrl0": form_data.get("MediaUrl0"),
            "MediaContentType0": form_data.get("MediaContentType0"),
            "ProfileName": form_data.get("ProfileName", ""),
            "MessageSid": form_data.get("MessageSid")
        }
