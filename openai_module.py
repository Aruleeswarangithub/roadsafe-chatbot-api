# openai_module.py
def classify_intent(message):
    """
    Classifies the user's message into an intent.
    Returns "weather" for weather-related queries, 
    "reststop" for rest stop-related queries, 
    and "unknown" for anything else.
    """
    message = message.lower()  # Ensure the message is case-insensitive
    if any(word in message for word in ["weather", "rain", "temperature"]):
        return "weather"
    elif any(word in message for word in ["rest stop", "parking", "cafe", "hotel", "fuel", "charging", "mechanic", "shop", "station", "place", "garage", "repair", "inn"]):
        return "reststop"
    return "unknown"