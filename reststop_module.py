# reststop_module.py
import requests

OVERPASS_URL = "http://overpass-api.de/api/interpreter"

# Supported amenities to match rest stop types
AMENITY_KEYWORDS = {
    "fuel": "fuel",
    "cafe": "cafe",
    "hotel": "hotel",
    "shop": "convenience",
    "charging": "charging_station",
    "mechanic": "car_repair",
    "parking": "parking"
}

def build_overpass_query(lat, lon, prefs):
    """Constructs an Overpass QL query based on preferences and location."""
    radius = 3000  # 3 km radius
    filters = []

    for pref in prefs:
        amenity = AMENITY_KEYWORDS.get(pref)
        if amenity:
            filters.append(f'node["amenity"="{amenity}"](around:{radius},{lat},{lon});')

    if not filters:
        return None

    query = f"""
    [out:json];
    (
        {"".join(filters)}
    );
    out body;
    """
    return query

def get_nearby_reststops(lat, lon, prefs):
    """Calls Overpass API to find nearby rest stops matching user preferences."""
    query = build_overpass_query(lat, lon, prefs)
    if not query:
        return "No supported preferences found."

    response = requests.post(OVERPASS_URL, data={"data": query})

    if response.status_code != 200:
        return "Failed to fetch data from Overpass API."

    data = response.json()
    elements = data.get("elements", [])

    if not elements:
        return "No suitable rest stops found nearby."

    stops = []
    for el in elements:
        name = el.get("tags", {}).get("name", "Unnamed")
        amenity = el.get("tags", {}).get("amenity", "Unknown")
        lat = el.get("lat")
        lon = el.get("lon")
        stops.append({
            "name": name,
            "type": amenity,
            "lat": lat,
            "lon": lon
        })

    return stops
