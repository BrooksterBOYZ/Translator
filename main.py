@app.route('/text-to-speech', methods=['POST'])
def handle_text_to_speech():
    try:
        # Get input text and target language from the request
        data = request.get_json()
        text = data['text']
        target_language = data.get('language', 'en')  # Default to English if no language provided

        print(f"Received text: {text}, Language: {target_language}")  # Debugging line

        # Translate the text to the target language
        translated_text = translate_text(text, target_language)

        print(f"Translated text: {translated_text}")  # Debugging line

        if "error" in translated_text.lower():
            return jsonify({'error': f"Translation failed: {translated_text}"}), 400

        # Convert translated text to speech
        text_to_speech(translated_text, target_language)

        return jsonify({'message': 'Text-to-Speech processing complete.'}), 200
    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error message
        return jsonify({'error': str(e)}), 400

