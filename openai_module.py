def classify_intent(message):
    if any(word in message for word in ["weather", "rain", "temperature"]):
        return "weather"
    elif any(word in message for word in ["rest stop", "parking", "cafe", "hotel", "fuel", "charging", "mechanic", "shop"]):
        return "reststop"
    return "unknown"
