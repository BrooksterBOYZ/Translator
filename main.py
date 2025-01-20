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

    # Default to English voice
    selected_voice = None

    for voice in voices:
        if language_code in voice.languages:
            selected_voice = voice
            break
    if not selected_voice:
        selected_voice = voices[0]  # fallback to default voice

    engine.setProperty('voice', selected_voice.id)
    engine.setProperty('rate', 150)  # Optional: adjust the speaking rate (words per minute)
    engine.setProperty('volume', 1)  # Optional: set the volume (0.0 to 1.0)
    
    # Actually make the engine speak
    engine.say(text)
    engine.runAndWait()

@app.route('/text-to-speech', methods=['POST'])
def handle_text_to_speech():
    try:
        # Get input text and target language from the request
        data = request.get_json()
        text = data['text']
        target_language = data.get('language', 'en')

        # Translate the text if needed
        translated_text = translate_text(text, target_language)

        # Convert translated text to speech
        text_to_speech(translated_text, target_language)

        return jsonify({'message': 'Text-to-Speech processing complete.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
