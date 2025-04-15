# app.py

from flask import Flask, request, jsonify
from reststop_module import get_nearby_reststops, choose_best_reststop
from weather_module import get_weather
from openai_module import classify_intent
from utils import get_greeting, user_preferences
import os
import logging

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Sandy Assistant API!"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()

    # ✅ Validate input
    if not data or "message" not in data or "lat" not in data or "lng" not in data:
        return jsonify({"reply": "Error: Missing required parameters (message, lat, lng)."}), 400

    message = data.get("message", "").lower()
    lat = data.get("lat")
    lon = data.get("lng")
    user_id = data.get("user_id", "default")
    prefs = user_preferences.get(user_id, user_preferences["default"])

    logging.info(f"📨 Message: '{message}' | 📍 Location: ({lat}, {lon}) | 👤 User: {user_id}")

    # 👂 Wake word
    if "hey sandy" in message:
        return jsonify({"reply": get_greeting()})

    # 🎯 Intent detection
    intent = classify_intent(message)

    # 🌤️ Weather
    if intent == "weather":
        logging.info("🌦️ Weather query")
        weather_info = get_weather(lat, lon)
        return jsonify({"reply": weather_info})

    # 🛑 Nearby rest stop search
    elif intent == "reststop":
        logging.info("🧭 Rest stop query")
        
        # Determine exact preference
        keywords = {
            "fuel": ["fuel", "petrol", "diesel"],
            "cafe": ["cafe", "coffee", "tea"],
            "hotel": ["hotel", "inn", "lodge"],
            "charging": ["ev", "charging", "charge"],
            "mechanic": ["mechanic", "repair", "garage"],
            "shop": ["shop", "store", "market"]
        }

        matched_prefs = []
        for key, terms in keywords.items():
            if any(word in message for word in terms):
                matched_prefs.append(key)

        if not matched_prefs:
            matched_prefs = prefs  # fallback to default if no specific preference

        reststops = get_nearby_reststops(lat, lon, matched_prefs)

        if isinstance(reststops, str):
            return jsonify({"reply": reststops})

        if not reststops:
            return jsonify({"reply": "Sorry, I couldn’t find any nearby places."})

        formatted = [f"{r['name']} ({r['distance']} km)" for r in reststops[:5]]
        list_output = "\n- " + "\n- ".join(formatted)
        return jsonify({
            "reply": f"Here are some nearby {matched_prefs[0]} places:{list_output}\nWhich one do you prefer?"
        })

    # ⭐ Best rest stop
    elif intent == "best_reststop":
        logging.info("🔝 Best rest stop requested")
        best = choose_best_reststop()
        if isinstance(best, str):
            return jsonify({"reply": best})
        return jsonify({
            "reply": f"The best option nearby is:\n{best['name']} ({best['distance']} km)"
        })

    # 🧠 Fallback
    logging.info("🤷 Unknown query")
    return jsonify({"reply": "I'm Sandy, your road assistant. Try asking about nearby fuel, cafes, hotels, or weather!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
