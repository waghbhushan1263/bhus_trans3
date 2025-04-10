from flask import Flask, request, jsonify
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

@app.route('/translate', methods=['POST'])
def translate_text():
    selected_text = request.json.get('text')
    lang = request.json.get('lang', 'mr')
    if not selected_text:
        return jsonify({'error': 'No text provided'}), 400
    translated = translator.translate(selected_text, dest=lang).text
    return jsonify({'translated_text': translated})

if __name__ == '__main__':
    app.run()
