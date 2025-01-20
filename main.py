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
    voice_id = voices[0].id  # Default to English voice

    # Try to match the language code to available voices
    for voice in voices:
        if language_code in voice.languages:
            voice_id = voice.id
            break

    engine.setProperty('voice', voice_id)

    # Save the audio to a file
    audio_filename = f"static/translated_audio_{uuid.uuid4().hex}.mp3"
    engine.save_to_file(text, audio_filename)
    engine.runAndWait()
    return audio_filename

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Translate route
@app.route('/translate', methods=['POST'])
def translate_route():
    data = request.get_json()
    text = data['text']
    target_lang = data['lang']

    # Translate the text
    translated_text = translate_text(text, target_lang)

    # Generate TTS for the translated text
    audio_filename = text_to_speech(translated_text, target_lang)

    return jsonify({
        'translated_text': translated_text,
        'audio_filename': audio_filename
    })

# Speech-to-text route (Optional, but implemented here for completeness)
@app.route('/speech_to_text', methods=['POST'])
def speech_to_text_route():
    # Placeholder implementation for speech-to-text (could be expanded with libraries like SpeechRecognition)
    return jsonify({'speech_text': 'Speech recognition is not implemented yet.'})

if __name__ == "__main__":
    app.run(debug=True)
