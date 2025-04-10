from flask import Flask, request, jsonify, render_template, Response
from googletrans import Translator
from io import BytesIO

app = Flask(__name__)
translator = Translator()

# Store PDF in memory (global for simplicity, reset per request in prod)
pdf_buffer = None

@app.route('/', methods=['GET', 'POST'])
def upload_pdf():
    global pdf_buffer
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            return "No file uploaded", 400
        pdf_file = request.files['pdf_file']
        if pdf_file.filename == '':
            return "No file selected", 400
        pdf_buffer = BytesIO(pdf_file.read())  # Store in memory
        return render_template('display.html')
    return render_template('index.html')

@app.route('/pdf', methods=['GET'])
def serve_pdf():
    global pdf_buffer
    if pdf_buffer is None:
        return "No PDF uploaded yet", 404
    pdf_buffer.seek(0)  # Reset buffer position
    return Response(pdf_buffer, mimetype='application/pdf')

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
