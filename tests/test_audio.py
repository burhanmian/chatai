import pytest
from app.audio.stt import WhisperSTT
from app.audio.tts import ElevenLabsTTS
from app.audio.processor import AudioProcessor


@pytest.mark.asyncio
async def test_audio_processor():
    """Test audio processor"""
    processor = AudioProcessor(cache_dir="/tmp/test_audio")
    
    # Test save audio
    test_data = b"test audio data"
    file_path = await processor.save_audio(test_data, format="mp3")
    
    assert file_path.endswith(".mp3")
    
    # Cleanup
    processor.cleanup(file_path)


def test_whisper_stt_init():
    """Test Whisper STT initialization"""
    stt = WhisperSTT(api_key="test_key")
    assert stt.client is not None


def test_elevenlabs_tts_init():
    """Test ElevenLabs TTS initialization"""
    tts = ElevenLabsTTS(api_key="test_key", voice_id="test_voice")
    assert tts.api_key == "test_key"
    assert tts.voice_id == "test_voice"
