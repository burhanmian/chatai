#!/usr/bin/env python3
"""
Voice message testing script
Tests the complete audio pipeline: STT -> Processing -> TTS
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.audio.stt import WhisperSTT
from app.audio.tts import ElevenLabsTTS
from app.audio.processor import AudioProcessor
from app.agents.orchestrator import AgentOrchestrator
from app.config import settings


async def test_voice_pipeline():
    """Test complete voice processing pipeline"""
    print("Testing DostAI Voice Pipeline")
    print("=" * 50)
    
    # Initialize components
    print("\n1. Initializing components...")
    
    try:
        whisper = WhisperSTT(settings.openai_api_key)
        print("   ✓ Whisper STT initialized")
        
        elevenlabs = ElevenLabsTTS(
            settings.elevenlabs_api_key,
            settings.elevenlabs_voice_id
        )
        print("   ✓ ElevenLabs TTS initialized")
        
        processor = AudioProcessor()
        print("   ✓ Audio Processor initialized")
        
        orchestrator = AgentOrchestrator(settings.openai_api_key)
        print("   ✓ Agent Orchestrator initialized")
        
    except Exception as e:
        print(f"   ✗ Initialization failed: {str(e)}")
        sys.exit(1)
    
    # Test text-to-speech
    print("\n2. Testing Text-to-Speech...")
    test_text = "Assalam-o-Alaikum! Main DostAI hoon, aap ki WhatsApp assistant."
    
    try:
        audio_bytes = await elevenlabs.speak(test_text)
        audio_path = await processor.save_audio(audio_bytes, format="mp3")
        print(f"   ✓ Audio generated: {audio_path}")
        print(f"   ✓ Audio size: {len(audio_bytes)} bytes")
        
        # Cleanup
        processor.cleanup(audio_path)
        
    except Exception as e:
        print(f"   ✗ TTS failed: {str(e)}")
    
    # Test orchestrator
    print("\n3. Testing Agent Orchestrator...")
    test_messages = [
        "Check my email",
        "Schedule a meeting tomorrow",
        "Make a JazzCash payment",
        "Pay my K-Electric bill"
    ]
    
    for message in test_messages:
        try:
            result = await orchestrator.process_message(message)
            print(f"   ✓ Message: {message}")
            print(f"     Route: {result['route_to_agent'] or 'general'}")
        except Exception as e:
            print(f"   ✗ Failed to process '{message}': {str(e)}")
    
    print("\n" + "=" * 50)
    print("✓ Voice pipeline testing completed!")


if __name__ == "__main__":
    asyncio.run(test_voice_pipeline())
