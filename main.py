from flask import Flask, render_template, request, jsonify
import pyttsx3
from deep_translator import GoogleTranslator
import uuid

# Initialize the Flask app
app = Flask(__name__)

# Initialize the TTS engine
engine = pyttsx3.init()

# Function to translate text using Google Translator
def translate_text(text, target_language):
    translated = GoogleTranslator(source='auto', target=target_language).translate(text)
    return translated

# Function to convert text to speech using pyttsx3
def text_to_speech(text, language_code):
    # Set the language for the TTS engine based on language_code
    voices = engine.getProperty('voices')
    # Default to English if language is not found
    voice_id
