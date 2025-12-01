from flask import Flask, render_template, request, jsonify
from emotion_engine import EmotionEngine

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')
engine = EmotionEngine()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '')
    result = engine.analyze(text)
    return jsonify(result)

if __name__ == '__main__':
    # Using port 5002 to avoid conflicts
    app.run(debug=True, port=5002)
