from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
import openai

app = Flask(__name__)
CORS(app)

# ✅ Your OpenAI project secret key
OPENAI_API_KEY = "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"
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

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

    try:
        response = client.chat.completions.create(
            model="gpt-4",  # or use "gpt-3.5-turbo" to save tokens
            messages=[
                {"role": "system", "content": "You are a legal summarization AI."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content
        return jsonify({"summary": answer})

    except Exception as e:
        print("❌ OpenAI API Error:", e)
        return jsonify({"error": "Failed to connect to OpenAI API."}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
