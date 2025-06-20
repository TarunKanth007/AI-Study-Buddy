from flask import Flask, request, jsonify, send_from_directory
from google import genai
import threading
import webbrowser

# Initialize Gemini client
genai_client = genai.Client(api_key="your-api-key")  # Replace with your actual key

# Flask setup
app = Flask(__name__, static_url_path='', static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    try:
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question
        )
        return jsonify({"response": response.text})
    except Exception as e:
        print("Chat Error:", e)
        return jsonify({"response": "Sorry, I couldn't get a response."}), 500

@app.route('/flashcards', methods=['POST'])
def flashcards():
    data = request.get_json()
    topic = data.get("topic", "")
    prompt = (
        f"Generate 5 flashcard-style questions and answers on the topic '{topic}'. "
        "Format each as:\nQ: question\nA: answer\n\n"
    )
    try:
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return jsonify({"cards": response.text})
    except Exception as e:
        print("Flashcard Error:", e)
        return jsonify({"cards": "Error generating flashcards."}), 500

@app.route('/quiz', methods=['POST'])
def quiz():
    data = request.get_json()
    topic = data.get("topic", "")
    prompt = (
        f"Generate 5 multiple-choice questions on '{topic}'. Each question should be formatted as:\n"
        "Q: ...\na) ...\nb) ...\nc) ...\nd) ...\nAnswer: ..."
    )
    try:
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return jsonify({"quiz": response.text})
    except Exception as e:
        print("Quiz Error:", e)
        return jsonify({"quiz": "Error generating quiz."}), 500

def open_browser():
    webbrowser.open("http://localhost:5000")

if __name__ == '__main__':
    threading.Timer(1.2, open_browser).start()
    app.run(debug=True)
