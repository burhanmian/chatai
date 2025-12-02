from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # OpenAI
    openai_api_key: str = "test_key"
    
    # ElevenLabs
    elevenlabs_api_key: str = "test_key"
    elevenlabs_voice_id: str = "test_voice"
    
    # Twilio
    twilio_account_sid: str = "test_sid"
    twilio_auth_token: str = "test_token"
    twilio_whatsapp_number: str = "whatsapp:+14155238886"
    
    # Database
    database_url: str = "sqlite+aiosqlite:///:memory:"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # JazzCash
    jazzcash_merchant_id: Optional[str] = None
    jazzcash_password: Optional[str] = None
    jazzcash_integrity_salt: Optional[str] = None
    jazzcash_return_url: Optional[str] = None
    
    # Easypaisa
    easypaisa_store_id: Optional[str] = None
    easypaisa_password: Optional[str] = None
    easypaisa_merchant_id: Optional[str] = None
    
    # Google APIs
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    google_redirect_uri: Optional[str] = None
    
    # Pinecone
    pinecone_api_key: Optional[str] = None
    pinecone_environment: Optional[str] = None
    
    # Application
    debug: bool = False
    log_level: str = "INFO"
    webhook_base_url: str = "http://localhost:8000"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
