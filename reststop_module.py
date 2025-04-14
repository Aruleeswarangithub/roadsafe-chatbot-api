# reststop_module.py
import requests
from math import radians, cos, sin, asin, sqrt

OVERPASS_API_URL = "http://overpass-api.de/api/interpreter"

# Supported preference mappings to OSM amenities
PREFERENCE_TO_OSM = {
    "fuel": "fuel",
    "cafe": "cafe",
    "hotel": "hotel",
    "charging": "charging_station",
    "mechanic": "car_repair",
    "shop": "shop"
}

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great-circle distance between two points.
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km

def get_nearby_reststops(lat, lon, prefs):
    elements = []
    for pref in prefs:
        if pref not in PREFERENCE_TO_OSM:
            continue
        osm_tag = PREFERENCE_TO_OSM[pref]
        query = f"""
        [out:json][timeout:25];
        (
          node["amenity"="{osm_tag}"](around:10000,{lat},{lon});
          way["amenity"="{osm_tag}"](around:10000,{lat},{lon});
          relation["amenity"="{osm_tag}"](around:10000,{lat},{lon});
        );
        out center;
        """
        response = requests.post(OVERPASS_API_URL, data={"data": query})
        if response.status_code == 200:
            elements += response.json().get("elements", [])
    
    reststops = []
    for el in elements:
        name = el.get("tags", {}).get("name", "Unnamed Location")
        el_lat = el.get("lat") or el.get("center", {}).get("lat")
        el_lon = el.get("lon") or el.get("center", {}).get("lon")
        distance = haversine(lon, lat, el_lon, el_lat)
        reststops.append({
            "name": name,
            "lat": el_lat,
            "lon": el_lon,
            "distance_km": round(distance, 2)
        })

    return sorted(reststops, key=lambda x: x["distance_km"])

def choose_best_reststop(lat, lon, prefs):
    """
    Chooses the closest rest stop from OSM results based on distance.
    """
    nearby = get_nearby_reststops(lat, lon, prefs)
    if not nearby:
        return "No suitable rest stops found."
    return nearby[0]
