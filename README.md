# DostAI - Pakistan's WhatsApp AI Assistant 🇵🇰

Pakistan's first **production-ready** proactive AI assistant with full audio support for WhatsApp.

## 🌟 Features

### 🎙️ Full Audio Support
- **Speech-to-Text**: OpenAI Whisper API for Urdu/English transcription
- **Text-to-Speech**: ElevenLabs multilingual voice synthesis
- **Audio Processing**: Complete pipeline for WhatsApp voice messages

### 💬 Multi-Language Support
- **Urdu** (اردو): Native Urdu script support
- **English**: Full English language support
- **Roman Urdu**: Phonetic Urdu in English characters

### 🤖 AI-Powered Agents
- **Email Agent**: Gmail integration for inbox management
- **Calendar Agent**: Google Calendar scheduling
- **Reminder Agent**: Proactive notifications and reminders
- **Payment Agent**: JazzCash & Easypaisa integration
- **Local Services Agent**: K-Electric, Careem, Foodpanda, Daraz

### 💳 Payment Integrations
- **JazzCash**: Mobile wallet payments (sandbox)
- **Easypaisa**: Mobile wallet payments (sandbox)
- **Utility Bills**: K-Electric, Sui Gas, WAPDA

### 🚀 Local Services
- **K-Electric**: Bill payments
- **Careem**: Ride booking assistance
- **Foodpanda**: Food ordering
- **Daraz**: Shopping assistance

## 📋 Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 15
- Redis 7
- FFmpeg (for audio processing)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/burhanmian/chatai.git
cd chatai
```

### 2. Configure Environment Variables

Copy the example environment file and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# ElevenLabs API
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=your_voice_id_here

# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Database
DATABASE_URL=postgresql://dostai:dostai@db:5432/dostai

# Redis
REDIS_URL=redis://redis:6379

# (Optional) Payment Providers
JAZZCASH_MERCHANT_ID=your_merchant_id_here
JAZZCASH_PASSWORD=your_password_here
# ... (see .env.example for all options)
```

### 3. Start with Docker Compose

```bash
docker-compose up -d
```

This will start:
- **API Server** (port 8000)
- **PostgreSQL Database** (port 5432)
- **Redis** (port 6379)
- **Celery Worker** (background tasks)

### 4. Initialize Database

```bash
docker-compose exec api python scripts/setup_db.py
```

### 5. Verify Installation

```bash
# Check API health
curl http://localhost:8000/health

# Check database connection
curl http://localhost:8000/health/db

# View API info
curl http://localhost:8000/api/info
```

## 📱 WhatsApp Configuration

### 1. Set Up Twilio WhatsApp Sandbox

1. Go to [Twilio Console](https://console.twilio.com/)
2. Navigate to **Messaging** > **Try it out** > **Send a WhatsApp message**
3. Follow instructions to join your WhatsApp sandbox
4. Note your sandbox number (e.g., `whatsapp:+14155238886`)

### 2. Configure Webhook

Set your webhook URL in Twilio:

```
https://your-domain.com/webhook
```

For local development, use ngrok:

```bash
ngrok http 8000
```

Then set the ngrok URL as your webhook:
```
https://your-ngrok-url.ngrok.io/webhook
```

### 3. Test Your Bot

Send a WhatsApp message to your Twilio sandbox number:

```
Hello DostAI
```

Expected response:
```
Assalam-o-Alaikum! Main DostAI hoon. Main aap ki kaise madad kar sakta hoon?
```

## 🧪 Testing

### Run Unit Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_audio.py

# Run with coverage
pytest tests/ --cov=app
```

### Test Voice Pipeline

```bash
python scripts/test_voice.py
```

This tests:
- Text-to-Speech with ElevenLabs
- Agent orchestrator routing
- Audio processing

## 🏗️ Architecture

```
┌─────────────────┐
│   WhatsApp      │
│   (Twilio)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI App   │
│   (main.py)     │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    ▼         ▼          ▼          ▼
┌────────┐ ┌──────┐ ┌────────┐ ┌────────┐
│ Audio  │ │Agents│ │Payment │ │Database│
│Pipeline│ │      │ │Gateway │ │        │
└────────┘ └──────┘ └────────┘ └────────┘
    │         │          │          │
    ▼         ▼          ▼          ▼
┌─────────────────────────────────────┐
│  OpenAI, ElevenLabs, JazzCash, etc. │
└─────────────────────────────────────┘
```

## 📂 Project Structure

```
chatai/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── celery_app.py        # Celery configuration
│   ├── api/                 # API endpoints
│   │   ├── webhooks.py      # Twilio webhook
│   │   ├── health.py        # Health checks
│   │   └── admin.py         # Admin endpoints
│   ├── audio/               # Audio processing
│   │   ├── stt.py           # Speech-to-Text (Whisper)
│   │   ├── tts.py           # Text-to-Speech (ElevenLabs)
│   │   ├── processor.py     # Audio processing
│   │   └── utils.py         # Audio utilities
│   ├── whatsapp/            # WhatsApp integration
│   │   ├── client.py        # Twilio client
│   │   ├── handlers.py      # Message handlers
│   │   └── media.py         # Media downloader
│   ├── agents/              # LangChain agents
│   │   ├── orchestrator.py  # Main orchestrator (GPT-4o)
│   │   ├── email_agent.py   # Email management
│   │   ├── calendar_agent.py# Calendar scheduling
│   │   ├── reminder_agent.py# Reminders
│   │   ├── payment_agent.py # Payment processing
│   │   └── local_services.py# Local services
│   ├── payments/            # Payment integrations
│   │   ├── jazzcash.py      # JazzCash API
│   │   ├── easypaisa.py     # Easypaisa API
│   │   └── bills.py         # Utility bills
│   ├── database/            # Database layer
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── crud.py          # CRUD operations
│   │   └── session.py       # DB session
│   └── utils/               # Utilities
│       ├── language.py      # Language detection
│       └── cache.py         # Redis caching
├── tests/                   # Test suite
├── scripts/                 # Setup scripts
├── docker-compose.yml       # Docker configuration
├── Dockerfile               # Docker image
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## 🔧 Development

### Local Development (without Docker)

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL and Redis locally**

3. **Run database migrations**:
   ```bash
   python scripts/setup_db.py
   ```

4. **Start the server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Start Celery worker** (in separate terminal):
   ```bash
   celery -A app.celery_app worker --loglevel=info
   ```

### API Endpoints

- `GET /` - Service information
- `GET /health` - Health check
- `GET /health/db` - Database health check
- `POST /webhook` - Twilio WhatsApp webhook
- `GET /api/info` - API information
- `GET /admin/users` - List users (admin)
- `GET /admin/conversations/{user_id}` - User conversations

## 🚀 Deployment

### Production Deployment

1. **Set up a production server** (Ubuntu 20.04+)

2. **Install Docker and Docker Compose**:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   ```

3. **Clone and configure**:
   ```bash
   git clone https://github.com/burhanmian/chatai.git
   cd chatai
   cp .env.example .env
   # Edit .env with production credentials
   ```

4. **Start services**:
   ```bash
   docker-compose up -d
   ```

5. **Set up reverse proxy** (Nginx):
   ```nginx
   server {
       listen 80;
       server_name dostai.yourdomain.com;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

6. **Enable HTTPS** (Let's Encrypt):
   ```bash
   certbot --nginx -d dostai.yourdomain.com
   ```

## 📊 Monitoring

### Logs

```bash
# View API logs
docker-compose logs -f api

# View Celery logs
docker-compose logs -f celery_worker

# View all logs
docker-compose logs -f
```

### Health Checks

```bash
# API health
curl https://your-domain.com/health

# Database health
curl https://your-domain.com/health/db
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **OpenAI** - Whisper STT & GPT-4o
- **ElevenLabs** - Multilingual TTS
- **Twilio** - WhatsApp Business API
- **LangChain** - Agent orchestration framework

## 📧 Support

For support, email support@dostai.pk or join our Slack channel.

---

**Built with ❤️ for 140M+ Pakistani WhatsApp users**

🚀 **DostAI - Aapka Digital Dost**