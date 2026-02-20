import requests

# Your Geoapify API Key
GEOAPIFY_KEY = "86f08bb48f934a8cbcc0de5564ea2c13"


# Get latitude and longitude from city name (GLOBAL)
def get_coordinates(city):

    url = f"https://api.geoapify.com/v1/geocode/search?text={city}&apiKey={GEOAPIFY_KEY}"

    response = requests.get(url)
    data = response.json()

    if not data.get("features"):
        return None, None

    lat = data["features"][0]["properties"]["lat"]
    lon = data["features"][0]["properties"]["lon"]

    return lat, lon


# Get real-time weather from Open-Meteo
def get_weather(city):

    lat, lon = get_coordinates(city)

    if lat is None:
        return {"error": "City not found"}

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

    response = requests.get(url)
    data = response.json()

    current = data["current_weather"]

    return {
        "city": city,
        "temperature": current["temperature"],
        "wind_speed": current["windspeed"],
        "wind_direction": current["winddirection"]
    }


# Test
if __name__ == "__main__":

    city = input("Enter city: ")
    result = get_weather(city)
    print(result)