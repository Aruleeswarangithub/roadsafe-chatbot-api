from flask import Flask, request, jsonify
from reststop_module import get_nearby_reststops, choose_best_reststop
from weather_module import get_weather
from openai_module import classify_intent
from utils import get_greeting, user_preferences
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Sandy Assistant API!"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()

    # Validate incoming data
    if not data or "message" not in data or "lat" not in data or "lng" not in data:
        return jsonify({"reply": "Error: Missing required parameters (message, lat, lng)."}), 400

    message = data.get("message", "").lower()
    lat = data.get("lat")
    lon = data.get("lng")
    user_id = data.get("user_id", "default")
    prefs = user_preferences.get(user_id, user_preferences["default"])

    logging.info(f"Received message: {message} from user: {user_id} at location ({lat}, {lon})")

    # 🌟 Wake word logic
    if "hey sandy" in message:
        logging.info("Wake word detected: 'hey sandy'")
        return jsonify({"reply": get_greeting()})

    intent = classify_intent(message)

    # 🌤️ Weather
    if intent == "weather":
        logging.info("Weather query detected")
        weather_info = get_weather(lat, lon)
        return jsonify({"reply": weather_info})

    # 🛑 Reststop handling
    elif intent == "reststop":
        logging.info("Rest stop query detected")
        reststops = get_nearby_reststops(lat, lon, prefs)
        if not reststops:
            return jsonify({"reply": "Sorry, I couldn’t find any nearby rest stops right now."})
        
        names = [r['name'] for r in reststops]
        names_str = ', '.join(names)
        return jsonify({"reply": f"Here are some nearby rest stops: {names_str}. Which one do you prefer?"})

    # 🤖 Follow-up: best rest stop
    elif "best" in message and "rest stop" in message:
        logging.info("Best rest stop query detected")
        best_stop = choose_best_reststop()
        if isinstance(best_stop, str):  # In case there are no suitable rest stops
            return jsonify({"reply": best_stop})
        return jsonify({"reply": f"Based on your preferences, I suggest: {best_stop['name']}. Ready to navigate?"})

    # 🧠 Default fallback
    logging.info("Fallback response")
    return jsonify({"reply": "I'm Sandy, your assistant. I can help with directions, weather, or nearby places!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Default to port 5000 if not set
    app.run(host='0.0.0.0', port=port, debug=True)
