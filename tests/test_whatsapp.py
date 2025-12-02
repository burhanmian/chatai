import pytest
from app.whatsapp.client import WhatsAppClient
from app.whatsapp.handlers import MessageHandler


def test_whatsapp_client_init():
    """Test WhatsApp client initialization"""
    client = WhatsAppClient(
        account_sid="test_sid",
        auth_token="test_token",
        whatsapp_number="whatsapp:+14155238886"
    )
    assert client.whatsapp_number == "whatsapp:+14155238886"


@pytest.mark.asyncio
async def test_message_handler_extract_sender():
    """Test message handler sender extraction"""
    handler = MessageHandler()
    
    message_data = {
        "From": "whatsapp:+923001234567",
        "ProfileName": "Test User"
    }
    
    sender_info = await handler.extract_sender_info(message_data)
    
    assert sender_info["phone_number"] == "+923001234567"
    assert sender_info["name"] == "Test User"


@pytest.mark.asyncio
async def test_message_handler_text():
    """Test handling text message"""
    handler = MessageHandler()
    
    message_data = {
        "From": "whatsapp:+923001234567",
        "Body": "Hello DostAI"
    }
    
    text = await handler.handle_text_message(message_data)
    
    assert text == "Hello DostAI"
