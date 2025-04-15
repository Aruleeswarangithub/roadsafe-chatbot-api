# openmapapi_module.py

def classify_intent(message):
    """
    Classifies the user's message into an intent.
    """
    message = message.lower()

    if any(word in message for word in ["weather", "rain", "temperature"]):
        return "weather"

    elif "which is best" in message or "best one" in message:
        return "best_reststop"

    elif any(word in message for word in [
        "fuel", "petrol", "gas", "cafe", "coffee", "hotel", "stay", "charging",
        "ev", "electric", "mechanic", "repair", "garage", "shop", "store", "rest stop", "station", "place"
    ]):
        return "reststop"

    return "unknown"


def extract_preference(message):
    """
    Extracts the specific rest stop category user asked for (e.g., 'fuel', 'cafe').
    """
    message = message.lower()

    if any(word in message for word in ["fuel", "petrol", "gas"]):
        return ["fuel"]
    elif any(word in message for word in ["cafe", "coffee"]):
        return ["cafe"]
    elif any(word in message for word in ["hotel", "inn", "stay"]):
        return ["hotel"]
    elif any(word in message for word in ["charging", "ev", "electric"]):
        return ["charging"]
    elif any(word in message for word in ["mechanic", "repair", "garage"]):
        return ["mechanic"]
    elif any(word in message for word in ["shop", "store"]):
        return ["shop"]
    else:
        return ["fuel", "cafe"]  # default preferences
