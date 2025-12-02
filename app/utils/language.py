import re
from typing import Optional


def detect_language(text: str) -> str:
    """
    Detect language of text (Urdu, English, or Roman Urdu)
    
    Args:
        text: Text to analyze
        
    Returns:
        Language code (ur, en, roman_urdu)
    """
    # Check for Urdu script
    urdu_pattern = re.compile(r'[\u0600-\u06FF]')
    if urdu_pattern.search(text):
        return "ur"
    
    # Check for common Roman Urdu patterns
    roman_urdu_words = [
        'aap', 'main', 'hain', 'hai', 'kya', 'kaise', 'kahan',
        'kyun', 'jab', 'ab', 'phir', 'yeh', 'woh', 'mujhe',
        'apko', 'humain', 'theek', 'acha', 'bura'
    ]
    
    text_lower = text.lower()
    roman_urdu_count = sum(1 for word in roman_urdu_words if word in text_lower)
    
    if roman_urdu_count >= 2:
        return "roman_urdu"
    
    # Default to English
    return "en"


def format_message_for_language(message: str, language: str) -> str:
    """
    Format message based on detected language
    
    Args:
        message: Message to format
        language: Target language
        
    Returns:
        Formatted message
    """
    # In production, you might want to add language-specific formatting
    return message


def translate_common_phrases(phrase: str, target_lang: str) -> str:
    """
    Translate common phrases to target language
    
    Args:
        phrase: Phrase to translate
        target_lang: Target language (ur, en, roman_urdu)
        
    Returns:
        Translated phrase
    """
    translations = {
        "hello": {
            "ur": "السلام علیکم",
            "en": "Hello",
            "roman_urdu": "Assalam-o-Alaikum"
        },
        "goodbye": {
            "ur": "خدا حافظ",
            "en": "Goodbye",
            "roman_urdu": "Khuda Hafiz"
        },
        "thank_you": {
            "ur": "شکریہ",
            "en": "Thank you",
            "roman_urdu": "Shukriya"
        },
        "please": {
            "ur": "براہ کرم",
            "en": "Please",
            "roman_urdu": "Barahe karam"
        }
    }
    
    phrase_lower = phrase.lower().replace(" ", "_")
    if phrase_lower in translations and target_lang in translations[phrase_lower]:
        return translations[phrase_lower][target_lang]
    
    return phrase
