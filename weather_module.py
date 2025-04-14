# weather_module.py
import requests

def get_weather(lat, lon):
    """
    Fetches the weather data from the OpenWeatherMap API.
    Returns a string with temperature and weather condition.
    """
    api_key = "dc6570fdefd02dcceb5465a24a89af9e"  # Your OpenWeatherMap API key
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url).json()
        if response.get("cod") != 200:  # Check for errors in the response
            return "Sorry, I couldn't fetch the weather data right now."
        
        temp = response["main"]["temp"]
        condition = response["weather"][0]["description"].capitalize()
        return f"The temperature is {temp}°C with {condition}."
    
    except Exception as e:
        return "Sorry, I couldn't fetch the weather data right now."
