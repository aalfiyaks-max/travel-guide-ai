import requests

def get_weather(city):

    # Step 1: Get coordinates using Geoapify (you already have this key)
    geo_url = "https://api.geoapify.com/v1/geocode/search"
    params = {
        "text": city + ", India",
        "apiKey": "86f08bb48f934a8cbcc0de5564ea2c13"
    }

    geo_response = requests.get(geo_url, params=params).json()

    lat = geo_response["features"][0]["properties"]["lat"]
    lon = geo_response["features"][0]["properties"]["lon"]

    # Step 2: Get real-time weather (NO API KEY needed)
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

    weather_response = requests.get(weather_url).json()

    current = weather_response["current_weather"]

    return {
        "city": city,
        "temperature": current["temperature"],
        "wind_speed": current["windspeed"],
        "time": current["time"]
    }

print(get_weather("Delhi"))