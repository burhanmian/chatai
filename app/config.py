from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # OpenAI
    openai_api_key: str
    
    # ElevenLabs
    elevenlabs_api_key: str
    elevenlabs_voice_id: str
    
    # Twilio
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_whatsapp_number: str
    
    # Database
    database_url: str
    
    # Redis
    redis_url: str
    
    # JazzCash
    jazzcash_merchant_id: Optional[str] = None
    jazzcash_password: Optional[str] = None
    jazzcash_integerity_salt: Optional[str] = None
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
    webhook_base_url: str
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
