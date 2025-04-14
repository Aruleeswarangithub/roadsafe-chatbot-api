def classify_intent(message):
    """
    Classifies the user's message into an intent.
    """
    message = message.lower()
    if any(word in message for word in ["weather", "rain", "temperature"]):
        return "weather"
    elif any(word in message for word in ["rest stop", "parking", "cafe", "hotel", "fuel", "charging", "mechanic", "shop", "station", "place", "garage", "repair", "inn"]):
        return "reststop"
    elif "which is best" in message or "best one" in message:
        return "best_reststop"
    return "unknown"
