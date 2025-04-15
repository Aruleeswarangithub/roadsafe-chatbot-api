# reststop_module.py

import requests
from math import radians, cos, sin, asin, sqrt

# Session-level memory
last_search_results = []

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculates the great circle distance between two points on the Earth (in km).
    """
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return R * 2 * asin(sqrt(a))

def get_nearby_reststops(lat, lon, prefs):
    """
    Uses OpenStreetMap Overpass API to fetch filtered places like fuel stations, cafes, etc.
    """
    global last_search_results
    last_search_results = []

    osm_tags = {
        "fuel": 'amenity=fuel',
        "cafe": 'amenity=cafe',
        "hotel": 'tourism=hotel',
        "charging": 'amenity=charging_station',
        "mechanic": 'shop=car_repair',
        "shop": 'shop=yes'
    }

    results = []

    for pref in prefs:
        if pref not in osm_tags:
            continue

        tag = osm_tags[pref]
        overpass_url = "http://overpass-api.de/api/interpreter"
        query = f"""
        [out:json];
        node[{tag}](around:3000,{lat},{lon});
        out body;
        """
        try:
            response = requests.get(overpass_url, params={"data": query}, timeout=10)
            data = response.json()
        except Exception as e:
            return f"Error fetching data: {e}"

        for element in data.get("elements", []):
            name = element.get("tags", {}).get("name", f"Unnamed {pref.title()}")
            distance_km = round(haversine(lat, lon, element["lat"], element["lon"]), 2)
            results.append({
                "name": name,
                "type": pref,
                "lat": element["lat"],
                "lon": element["lon"],
                "distance": distance_km
            })

    results.sort(key=lambda x: x["distance"])
    last_search_results = results

    return results if results else "Sorry, I couldn't find any nearby results for that."

def choose_best_reststop():
    """
    Returns the closest rest stop from the last search.
    """
    global last_search_results
    if not last_search_results:
        return "Please search for nearby places first."
    return last_search_results[0]
