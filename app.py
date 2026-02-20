from flask import Flask, render_template, request, jsonify
import requests
import json
import random

# Create Flask app
app = Flask(__name__)

# Your Geoapify API key
GEOAPIFY_KEY = "86f08bb48f934a8cbcc0de5564ea2c13"

# Load dataset
with open("places.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# WEATHER API
@app.route("/weather")
def weather():

    city = request.args.get("city")

    geo_url = f"https://api.geoapify.com/v1/geocode/search?text={city},India&apiKey={GEOAPIFY_KEY}"
    geo_response = requests.get(geo_url).json()

    lat = geo_response["features"][0]["properties"]["lat"]
    lon = geo_response["features"][0]["properties"]["lon"]

    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    weather_response = requests.get(weather_url).json()

    current = weather_response["current_weather"]

    return jsonify({
        "city": city,
        "temperature": current["temperature"],
        "wind_speed": current["windspeed"]
    })


# TOURIST PLACES API WITH REAL IMAGES
@app.route("/places")
def places():

    city = request.args.get("city")

    geo_url = f"https://api.geoapify.com/v1/geocode/search?text={city},India&apiKey={GEOAPIFY_KEY}"
    geo_response = requests.get(geo_url).json()

    lat = geo_response["features"][0]["properties"]["lat"]
    lon = geo_response["features"][0]["properties"]["lon"]

    url = f"https://api.geoapify.com/v2/places?categories=tourism&filter=circle:{lon},{lat},5000&limit=5&apiKey={GEOAPIFY_KEY}"

    response = requests.get(url).json()

    result = []

    for item in response.get("features", []):

        props = item["properties"]

        place_lat = props.get("lat")
        place_lon = props.get("lon")

        image_url = f"https://maps.geoapify.com/v1/staticmap?style=osm-carto&width=600&height=400&center=lonlat:{place_lon},{place_lat}&zoom=15&apiKey={GEOAPIFY_KEY}"

        result.append({
            "name": props.get("name", "Tourist Place"),
            "image": image_url
        })

    return jsonify(result)


# AI RECOMMENDATION WITH REAL IMAGES
@app.route("/recommend")
def recommend():

    budget = int(request.args.get("budget"))

    filtered = [place for place in dataset if place["budget"] <= budget]

    if len(filtered) >= 5:
        recommendations = random.sample(filtered, 5)
    else:
        recommendations = filtered

    result = []

    for place in recommendations:

        place_name = place["name"]

        geo_url = f"https://api.geoapify.com/v1/geocode/search?text={place_name},India&apiKey={GEOAPIFY_KEY}"

        geo_response = requests.get(geo_url).json()

        if geo_response.get("features"):

            lat = geo_response["features"][0]["properties"]["lat"]
            lon = geo_response["features"][0]["properties"]["lon"]

            image_url = f"https://maps.geoapify.com/v1/staticmap?style=osm-carto&width=600&height=400&center=lonlat:{lon},{lat}&zoom=15&apiKey={GEOAPIFY_KEY}"

        else:

            image_url = "https://via.placeholder.com/600x400?text=Travel+Place"

        result.append({
            "name": place_name,
            "budget": place["budget"],
            "image": image_url
        })

    return jsonify(result)


# HOTELS API WITH REAL IMAGES
@app.route("/hotels")
def hotels():

    city = request.args.get("city")
    budget = int(request.args.get("budget"))

    geo_url = f"https://api.geoapify.com/v1/geocode/search?text={city},India&apiKey={GEOAPIFY_KEY}"
    geo_response = requests.get(geo_url).json()

    lat = geo_response["features"][0]["properties"]["lat"]
    lon = geo_response["features"][0]["properties"]["lon"]

    hotel_url = f"https://api.geoapify.com/v2/places?categories=accommodation.hotel&filter=circle:{lon},{lat},5000&limit=10&apiKey={GEOAPIFY_KEY}"

    response = requests.get(hotel_url).json()

    result = []

    for item in response.get("features", []):

        props = item["properties"]

        hotel_budget = random.randint(1, 5)

        if hotel_budget <= budget:

            hotel_lat = props.get("lat")
            hotel_lon = props.get("lon")

            image_url = f"https://maps.geoapify.com/v1/staticmap?style=osm-carto&width=600&height=400&center=lonlat:{hotel_lon},{hotel_lat}&zoom=15&apiKey={GEOAPIFY_KEY}"

            result.append({
                "name": props.get("name", "Hotel"),
                "budget": hotel_budget,
                "image": image_url
            })

    return jsonify(result)


# RUN SERVER
if __name__ == "__main__":
    app.run(debug=True)