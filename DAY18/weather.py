import requests

def fetch_weather(city):
    api_key = 'your_openweather_api_key_here'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data['cod'] != 200:
            print("Failed to retrieve weather data.")
            return
        
        city_name = data['name']
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        
        print(f"Weather in {city_name}: {temp}°C, {description.capitalize()}")
    except Exception as e:
        print(f"An error occurred: {e}")
