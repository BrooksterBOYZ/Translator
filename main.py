from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pyttsx3
from deep_translator import GoogleTranslator
import uuid

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the TTS engine
engine = pyttsx3.init()

# Function to translate text using Google Translator
def translate_text(text, target_language):
    try:
        # Translate using Google Translator
        translated = GoogleTranslator(source='auto', target=target_language).translate(text)
        return translated
    except Exception as e:
        return str(e)

# Function to convert text to speech using pyttsx3
def text_to_speech(text, language_code):
    voices = engine.getProperty('voices')
    
    # Try to find a matching voice for the given language code
    selected_voice = None
    for voice in voices:
        if language_code.lower() in voice.languages:
            selected_voice = voice
            break
    
    # If no matching voice is found, fall back to the first available voice
    if not selected_voice:
        selected_voice = voices[0]
    
    # Set the selected voice
    engine.setProperty('voice', selected_voice.id)
    engine.setProperty('rate', 150)  # Optional: adjust speaking rate
    engine.setProperty('volume', 1)  # Optional: set the volume

    print(f"Using voice: {selected_voice.name} for language {language_code}")
    
    # Make the engine speak the text
    engine.say(text)
    engine.runAndWait()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/text-to-speech', methods=['POST'])
def handle_text_to_speech():
    try:
        # Get input text and target language from the request
        data = request.get_json()
        text = data['text']
        target_language = data.get('language', 'en')  # Default to English if no language provided

        # Translate the text to the target language
        translated_text = translate_text(text, target_language)

        if "error" in translated_text.lower():
            return jsonify({'error': f"Translation failed: {translated_text}"}), 400

        # Convert translated text to speech
        text_to_speech(translated_text, target_language)

        return jsonify({'message': 'Text-to-Speech processing complete.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
