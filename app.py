from flask import Flask, render_template, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from mcq_generator import generate_mcqs
from roadmap_generator import generate_roadmap

app = Flask(__name__)

# Rate Limiting
limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])

@app.route('/')
def index():
    return render_template('index.html')

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
        print("[DEBUG] MCQs generated:", mcqs)

        if not mcqs:
            return jsonify({'error': 'No MCQs generated for the given topic'}), 500

        return jsonify({'mcqs': mcqs})
    except Exception as e:
        print("[ERROR] Exception occurred:", str(e))
        return jsonify({'error': 'An internal error occurred'}), 500


@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    answers = data.get('answers')
    topic = data.get('topic')
    score = sum(1 for q in answers if q['user_answer'] == q['correct_answer'])
    roadmap = generate_roadmap(topic, score, len(answers))
    return jsonify({
        'score': score,
        'total': len(answers),
        'roadmap': roadmap
    })

if __name__ == '__main__':
    app.run(debug=True)
