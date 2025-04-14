import requests

def get_weather(lat, lon):
    api_key = "dc6570fdefd02dcceb5465a24a89af9e"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    temp = response["main"]["temp"]
    condition = response["weather"][0]["description"].capitalize()
    return f"The temperature is {temp}°C with {condition}."
