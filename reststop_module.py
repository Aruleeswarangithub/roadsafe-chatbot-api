import requests
from math import radians, cos, sin, asin, sqrt

# Store session-level memory of last search results
last_search_results = []

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculates the great circle distance (in km) between two points.
    """
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return R * 2 * asin(sqrt(a))

def get_nearby_reststops(lat, lon, prefs):
    """
    Uses OpenStreetMap Overpass API to fetch POIs like fuel stations, cafes, etc.
    Stores results for later ranking.
    """
    global last_search_results
    last_search_results = []  # Clear previous

    # Map user preferences to OSM tags
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
        res = requests.get(overpass_url, params={"data": query})
        data = res.json()

        for element in data.get("elements", []):
            name = element.get("tags", {}).get("name", f"Unnamed {pref.title()}")
            dist = round(haversine(lat, lon, element["lat"], element["lon"]), 2)
            results.append({
                "name": name,
                "type": pref,
                "lat": element["lat"],
                "lon": element["lon"],
                "distance": dist
            })

    # Sort by distance
    results.sort(key=lambda x: x["distance"])
    last_search_results = results  # Save for ranking later
    return results if results else "No nearby rest stops found."

def choose_best_reststop():
    """
    Returns the closest option from last_search_results.
    """
    global last_search_results
    if not last_search_results:
        return "Please ask for nearby places first!"
    return last_search_results[0]
