import os
import requests
import json
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_limiter import Limiter

load_dotenv()

app = Flask(__name__)
limiter = Limiter(key_func=lambda: request.remote_addr)  # Initialize Limiter without app
limiter.init_app(app)  # Bind Limiter to the Flask app

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Load the Gemini API key from .env

def generate_mcqs(topic):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"Generate 10 multiple choice questions (from easy to hard) on the topic '{topic}'. Each question should be a JSON object with this format: {{\"question\": \"...\", \"options\": [\"A\", \"B\", \"C\", \"D\"], \"correct_answer\": \"A\"}}. Respond with a JSON array of 10 such questions only. No explanation."}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for HTTP status codes 4xx/5xx
        content = response.json()
        print("[DEBUG] Gemini API raw response:", content)

        # Extract the generated content
        generated_text = content.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        print("[DEBUG] Extracted text:", generated_text)

        # Remove code block markers (```json and ```)
        if generated_text.startswith("```json"):
            generated_text = generated_text[7:]  # Remove the leading ```json
        if generated_text.endswith("```"):
            generated_text = generated_text[:-3]  # Remove the trailing ```

        # Parse the JSON response
        mcqs = json.loads(generated_text.strip())  # Strip any extra whitespace
        return mcqs
    except json.JSONDecodeError as json_error:
        print("[ERROR] Failed to parse JSON response:", json_error)
        return []
    except requests.exceptions.RequestException as e:
        print("[ERROR] Gemini API request failed:", e)
        return []

@app.route('/get_mcqs', methods=['POST'])
@limiter.limit("3 per minute")
def get_mcqs():
    try:
        data = request.json
        topic = data.get('topic')
        print("[DEBUG] Topic selected:", topic)

        if not topic:
            return jsonify({'error': 'Topic is required'}), 400

        mcqs = generate_mcqs(topic)
        if isinstance(mcqs, dict) and 'error' in mcqs:
            return jsonify(mcqs), 429  # Return a 429 status code for quota errors

        if not mcqs:
            return jsonify({'error': 'No MCQs generated for the given topic'}), 500

        return jsonify({'mcqs': mcqs})
    except Exception as e:
        print("[ERROR] Exception occurred:", str(e))
        return jsonify({'error': 'An internal error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)