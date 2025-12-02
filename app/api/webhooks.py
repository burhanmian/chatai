from fastapi import APIRouter, Request, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import logging

from app.database.session import get_db
from app.database import crud, schemas, models
from app.whatsapp.handlers import MessageHandler
from app.whatsapp.client import WhatsAppClient
from app.whatsapp.media import MediaDownloader
from app.audio.stt import WhisperSTT
from app.audio.tts import ElevenLabsTTS
from app.audio.processor import AudioProcessor
from app.agents.orchestrator import AgentOrchestrator
from app.agents.email_agent import EmailAgent
from app.agents.calendar_agent import CalendarAgent
from app.agents.reminder_agent import ReminderAgent
from app.agents.payment_agent import PaymentAgent
from app.agents.local_services import LocalServicesAgent
from app.payments.jazzcash import JazzCashClient
from app.payments.easypaisa import EasypaisaClient
from app.payments.bills import BillPaymentService
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize clients and services
whatsapp_client = WhatsAppClient(
    settings.twilio_account_sid,
    settings.twilio_auth_token,
    settings.twilio_whatsapp_number
)

message_handler = MessageHandler()
media_downloader = MediaDownloader(
    settings.twilio_account_sid,
    settings.twilio_auth_token
)

whisper_stt = WhisperSTT(settings.openai_api_key)
elevenlabs_tts = ElevenLabsTTS(
    settings.elevenlabs_api_key,
    settings.elevenlabs_voice_id
)
audio_processor = AudioProcessor()

# Initialize agents
orchestrator = AgentOrchestrator(settings.openai_api_key)
email_agent = EmailAgent()
calendar_agent = CalendarAgent()
reminder_agent = ReminderAgent()

# Initialize payment clients
jazzcash_client = None
if settings.jazzcash_merchant_id:
    jazzcash_client = JazzCashClient(
        settings.jazzcash_merchant_id,
        settings.jazzcash_password,
        settings.jazzcash_integrity_salt,
        settings.jazzcash_return_url
    )

easypaisa_client = None
if settings.easypaisa_store_id:
    easypaisa_client = EasypaisaClient(
        settings.easypaisa_store_id,
        settings.easypaisa_password,
        settings.easypaisa_merchant_id
    )

payment_agent = PaymentAgent(jazzcash_client, easypaisa_client)
bill_service = BillPaymentService()
local_services_agent = LocalServicesAgent(bill_service)


@router.post("/webhook")
async def whatsapp_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Twilio WhatsApp webhook endpoint
    Handles incoming text and voice messages
    """
    try:
        # Parse form data
        form_data = await request.form()
        message_data = message_handler.parse_webhook_data(dict(form_data))
        
        logger.info(f"Received webhook: {message_data}")
        
        # Extract sender info
        sender_info = await message_handler.extract_sender_info(message_data)
        phone_number = sender_info["phone_number"]
        
        # Get or create user
        user = await crud.get_user_by_phone(db, phone_number)
        if not user:
            user = await crud.create_user(
                db,
                schemas.UserCreate(
                    phone_number=phone_number,
                    name=sender_info.get("name"),
                    language_preference=models.LanguagePreference.ENGLISH
                )
            )
        
        # Check if it's a voice message
        voice_url = await message_handler.handle_voice_message(message_data)
        
        if voice_url:
            # Handle voice message
            logger.info(f"Processing voice message from {phone_number}")
            
            try:
                # Download audio
                audio_bytes = await media_downloader.download_media(voice_url)
                audio_path = await audio_processor.save_audio(audio_bytes, format="ogg")
                
                # Transcribe with Whisper
                transcript = await whisper_stt.transcribe_auto_detect(audio_path)
                logger.info(f"Transcribed: {transcript}")
                
                # Process with orchestrator
                result = await orchestrator.process_message(transcript, {
                    "user_id": user.id,
                    "language": user.language_preference.value
                })
                
                # Generate audio response
                audio_response = await elevenlabs_tts.speak(result["response"])
                response_audio_path = await audio_processor.save_audio(
                    audio_response,
                    format="mp3"
                )
                
                # Convert to OGG for WhatsApp
                ogg_path = audio_processor.convert_to_ogg(response_audio_path)
                
                # Send voice response (in production, upload to accessible URL)
                await whatsapp_client.send_text_message(
                    message_data["From"],
                    result["response"]
                )
                
                # Store conversation
                await crud.create_conversation(
                    db,
                    schemas.ConversationCreate(
                        user_id=user.id,
                        message_type=models.MessageType.AUDIO,
                        user_message=transcript,
                        ai_response=result["response"],
                        audio_transcript=transcript
                    )
                )
                
                # Cleanup
                audio_processor.cleanup(audio_path)
                audio_processor.cleanup(response_audio_path)
                audio_processor.cleanup(ogg_path)
                
            except Exception as e:
                logger.error(f"Voice processing error: {str(e)}")
                await whatsapp_client.send_text_message(
                    message_data["From"],
                    "Maaf kijiye, voice message process karne mein masla ho gaya."
                )
        
        else:
            # Handle text message
            text_message = await message_handler.handle_text_message(message_data)
            logger.info(f"Processing text message from {phone_number}: {text_message}")
            
            # Process with orchestrator
            result = await orchestrator.process_message(text_message, {
                "user_id": user.id,
                "language": user.language_preference.value
            })
            
            # Send response
            await whatsapp_client.send_text_message(
                message_data["From"],
                result["response"]
            )
            
            # Store conversation
            await crud.create_conversation(
                db,
                schemas.ConversationCreate(
                    user_id=user.id,
                    message_type=models.MessageType.TEXT,
                    user_message=text_message,
                    ai_response=result["response"]
                )
            )
        
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return {"status": "error", "message": str(e)}


@router.get("/webhook")
async def whatsapp_webhook_verification(request: Request):
    """Webhook verification endpoint for Twilio"""
    return {"status": "ok"}
