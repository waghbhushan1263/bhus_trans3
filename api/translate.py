from flask import Flask, request, jsonify, render_template, Response
from googletrans import Translator
from io import BytesIO

app = Flask(__name__, template_folder='../public')  # Point to public/
translator = Translator()

pdf_buffer = None

@app.route('/', methods=['GET', 'POST'])
def upload_pdf():
    global pdf_buffer
    try:
        if request.method == 'POST':
            if 'pdf_file' not in request.files:
                return "No file uploaded", 400
            pdf_file = request.files['pdf_file']
            if pdf_file.filename == '':
                return "No file selected", 400
            pdf_buffer = BytesIO(pdf_file.read())
            print("PDF uploaded, size:", pdf_buffer.getbuffer().nbytes)
            return render_template('display.html')
        return render_template('index.html')
    except Exception as e:
        print(f"Error in upload_pdf: {str(e)}")
        return f"Server error: {str(e)}", 500

@app.route('/api/pdf', methods=['GET'])
def serve_pdf():
    global pdf_buffer
    try:
        if pdf_buffer is None:
            print("No PDF buffer available")
            return "No PDF uploaded yet", 404
        pdf_buffer.seek(0)
        print("Serving PDF, size:", pdf_buffer.getbuffer().nbytes)
        return Response(pdf_buffer, mimetype='application/pdf')
    except Exception as e:
        print(f"Error in serve_pdf: {str(e)}")
        return f"Server error: {str(e)}", 500

@app.route('/api/translate', methods=['POST'])
def translate_text():
    try:
        selected_text = request.json.get('text')
        lang = request.json.get('lang', 'mr')
        if not selected_text:
            return jsonify({'error': 'No text provided'}), 400
        translated = translator.translate(selected_text, dest=lang).text
        print(f"Translated '{selected_text}' to '{translated}'")
        return jsonify({'translated_text': translated})
    except Exception as e:
        print(f"Error in translate_text: {str(e)}")
        return f"Server error: {str(e)}", 500

if __name__ == '__main__':
    app.run()
