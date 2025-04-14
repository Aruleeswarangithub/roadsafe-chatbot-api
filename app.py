from flask import Flask, request, jsonify
from reststop_module import get_nearby_reststops, choose_best_reststop
from weather_module import get_weather
from openai_module import classify_intent
from utils import get_greeting, user_preferences

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get("message", "").lower()
    lat = data.get("lat")
    lon = data.get("lng")
    user_id = data.get("user_id", "default")
    prefs = user_preferences.get(user_id, user_preferences["default"])

    # 🌟 Wake word logic
    if "hey sandy" in message:
        return jsonify({"reply": get_greeting()})

    intent = classify_intent(message)

    # 🌤️ Weather
    if intent == "weather":
        weather_info = get_weather(lat, lon)
        return jsonify({"reply": weather_info})

    # 🛑 Reststop handling
    elif intent == "reststop":
        reststops = get_nearby_reststops(lat, lon, prefs)
        if not reststops:
            return jsonify({"reply": "Sorry, I couldn’t find any nearby rest stops right now."})
        names = [r['name'] for r in reststops]
        names_str = ', '.join(names)
        return jsonify({"reply": f"Here are some nearby rest stops: {names_str}. Which one do you prefer?"})

    # 🤖 Follow-up: best rest stop
    elif "best" in message and "rest stop" in message:
        best_stop = choose_best_reststop(lat, lon, prefs)
        return jsonify({"reply": f"Based on your preferences, I suggest: {best_stop['name']}. Ready to navigate?"})

    # 🧠 Default fallback
    return jsonify({"reply": "I'm Sandy, your assistant. I can help with directions, weather, or nearby places!"})

if __name__ == '__main__':
    app.run(debug=True)
