import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

# Load environment variables and configure the API
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

# Create the model
generation_config = {
    "temperature": float(os.getenv("TEMPERATURE")),
    "top_p": float(os.getenv("TOP_P")),
    "top_k": int(os.getenv("TOP_K")),
    "max_output_tokens": int(os.getenv("MAX_OUTPUT_TOKENS")),
}

model = genai.GenerativeModel(
    model_name=os.getenv("MODEL_NAME"),
    generation_config=generation_config,
)

# Initialize Flask app
app = Flask(__name__)

# Store chat sessions
chat_sessions = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    session_id = request.json['session_id']

    if session_id not in chat_sessions:
        chat_sessions[session_id] = model.start_chat()

    chat_session = chat_sessions[session_id]

    try:
        response = chat_session.send_message(user_input)
        return jsonify({'response': response.text.strip()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)