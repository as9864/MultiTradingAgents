import os
from googletrans import Translator

translator = Translator()

def translate_text(text: str, target_lang: str = "ko") -> str:
    try:
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except Exception as e:
        print(f"❌ Translation error: {e}")
        return text