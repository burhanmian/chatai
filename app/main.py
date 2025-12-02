from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.database.session import init_db
from app.api import webhooks, health, admin

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting DostAI application...")
    try:
        await init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down DostAI application...")


# Create FastAPI app
app = FastAPI(
    title="DostAI - Pakistan's WhatsApp AI Assistant",
    description="Complete WhatsApp AI assistant with audio support, payments, and local services",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(webhooks.router, tags=["webhooks"])
app.include_router(admin.router, tags=["admin"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "DostAI",
        "version": "1.0.0",
        "description": "Pakistan's first proactive WhatsApp AI assistant",
        "features": [
            "Voice messages in Urdu/English/Roman Urdu",
            "JazzCash & Easypaisa payments",
            "Email & Calendar management",
            "Proactive reminders",
            "Local services (K-Electric, Careem, Foodpanda, Daraz)"
        ],
        "status": "operational"
    }


@app.get("/api/info")
async def api_info():
    """API information endpoint"""
    return {
        "name": "DostAI API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "webhook": "/webhook",
            "admin": "/admin"
        },
        "features": {
            "audio": {
                "stt": "OpenAI Whisper",
                "tts": "ElevenLabs",
                "languages": ["Urdu", "English", "Roman Urdu"]
            },
            "payments": {
                "providers": ["JazzCash", "Easypaisa"],
                "bill_payments": ["K-Electric", "Sui Gas", "WAPDA"]
            },
            "integrations": {
                "whatsapp": "Twilio",
                "email": "Gmail API",
                "calendar": "Google Calendar"
            },
            "local_services": [
                "Careem (ride booking)",
                "Foodpanda (food delivery)",
                "Daraz (shopping)"
            ]
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
