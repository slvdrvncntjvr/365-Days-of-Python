import requests

def get_weather(city, api_key):
    url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"
    response = requests.get(url)
    data = response.json()

    if "current" in data:
        temperature = data["current"]["temperature"]  
        description = data["current"]["weather_descriptions"][0]  
        return temperature, description
    else:
        return None
