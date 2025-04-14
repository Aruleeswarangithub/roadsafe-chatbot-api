# reststop_module.py
import random

def get_nearby_reststops(lat, lon, prefs):
    """
    Returns a list of nearby rest stops based on the user's preferences.
    The preferences can include "fuel", "cafe", "hotel", etc.
    """
    # Stubbed rest stops data (this could come from an API or database)
    all_reststops = [
        {"name": "Fuel & Cafe Stop", "type": ["fuel", "cafe"], "rating": 4.5},
        {"name": "Highway Hotel", "type": ["hotel"], "rating": 4.0},
        {"name": "Quick Garage", "type": ["mechanic"], "rating": 3.8},
        {"name": "EV Fast Charge", "type": ["charging"], "rating": 4.2},
        {"name": "Highway ShopZone", "type": ["shop"], "rating": 4.1},
    ]
    
    # Filter based on user preferences
    filtered = [stop for stop in all_reststops if any(p in stop["type"] for p in prefs)]
    
    # Return a message if no rest stops match the preferences
    if not filtered:
        return "No suitable rest stops found."
    
    return filtered

def choose_best_reststop(lat, lon, prefs):
    """
    Chooses the best rest stop based on the highest rating.
    Returns the best rest stop.
    """
    options = get_nearby_reststops(lat, lon, prefs)
    
    # Check if no options were returned
    if isinstance(options, str):  # In case we got the "No suitable rest stops found."
        return options
    
    best_stop = max(options, key=lambda x: x["rating"])
    return best_stop
