from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import fitz  # PyMuPDF
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__, static_folder='../front end', static_url_path='/')
CORS(app)

# Get OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Serve the index.html file at root
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Extract text from PDF using PyMuPDF
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Analyze PDF via POST request
@app.route('/analyze', methods=['POST'])
def analyze():
    pdf = request.files['pdf']
    text = extract_text_from_pdf(pdf)

    prompt = f"""
You're an expert legal assistant. Break down the following legal document into:
1. A plain-English summary of each section.
2. Any potential risks, confusing terms, or red flags.

Here is the document text:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You're a legal summarization AI."},
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content
    return jsonify({"summary": answer})

if __name__ == '__main__':
    app.run(debug=True)
