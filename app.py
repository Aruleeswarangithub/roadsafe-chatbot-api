from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allow requests from any origin (for mobile/web Flutter apps)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get("message", "No message provided")
    lat = data.get("lat", "0.0")
    lng = data.get("lng", "0.0")

    # Dummy response - Replace this with Groq/OpenAI/logic later
    reply = f"🤖 Hello! You said: '{message}'. Your location is ({lat}, {lng}). Stay safe on the road! 🛣️"

    return jsonify({"reply": reply})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # For Render compatibility
    app.run(host='0.0.0.0', port=port)
