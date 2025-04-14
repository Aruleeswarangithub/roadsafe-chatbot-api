import random

def get_nearby_reststops(lat, lon, prefs):
    # Stubbed rest stops
    all_reststops = [
        {"name": "Fuel & Cafe Stop", "type": ["fuel", "cafe"], "rating": 4.5},
        {"name": "Highway Hotel", "type": ["hotel"], "rating": 4.0},
        {"name": "Quick Garage", "type": ["mechanic"], "rating": 3.8},
        {"name": "EV Fast Charge", "type": ["charging"], "rating": 4.2},
        {"name": "Highway ShopZone", "type": ["shop"], "rating": 4.1},
    ]
    filtered = [stop for stop in all_reststops if any(p in stop["type"] for p in prefs)]
    return filtered

def choose_best_reststop(lat, lon, prefs):
    options = get_nearby_reststops(lat, lon, prefs)
    return max(options, key=lambda x: x["rating"])
