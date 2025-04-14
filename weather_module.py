# weather_module.py
import requests

def get_weather(lat, lon):
    """
    Fetches weather details based on the given latitude and longitude.
    """
    api_key = "dc6570fdefd02dcceb5465a24a89af9e"
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        return f"The current temperature is {temp}°C with {weather_desc}."
    else:
        return "Sorry, I couldn't fetch weather information right now."
