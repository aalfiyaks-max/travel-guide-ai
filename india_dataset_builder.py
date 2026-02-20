import requests
import json
import random
import time

API_KEY = "86f08bb48f934a8cbcc0de5564ea2c13"

# Major Indian cities (covering whole India)
locations = [
    ("Delhi", 28.6139, 77.2090),
    ("Mumbai", 19.0760, 72.8777),
    ("Bangalore", 12.9716, 77.5946),
    ("Chennai", 13.0827, 80.2707),
    ("Kolkata", 22.5726, 88.3639),
    ("Hyderabad", 17.3850, 78.4867),
    ("Jaipur", 26.9124, 75.7873),
    ("Goa", 15.2993, 74.1240),
    ("Agra", 27.1767, 78.0081),
    ("Varanasi", 25.3176, 82.9739),
    ("Kochi", 9.9312, 76.2673),
    ("Munnar", 10.0889, 77.0595),
    ("Shimla", 31.1048, 77.1734),
    ("Manali", 32.2432, 77.1892),
    ("Darjeeling", 27.0410, 88.2663),
    ("Amritsar", 31.6340, 74.8723),
    ("Udaipur", 24.5854, 73.7125),
    ("Mysore", 12.2958, 76.6394),
    ("Ooty", 11.4064, 76.6932),
    ("Leh", 34.1526, 77.5771)
]

places = []
seen = set()

for city, lat, lon in locations:

    print("Collecting from:", city)

    url = f"https://api.geoapify.com/v2/places?categories=tourism&filter=circle:{lon},{lat},50000&limit=100&apiKey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    for item in data["features"]:

        name = item["properties"].get("name")

        if name and name not in seen:

            seen.add(name)

            place = {
                "name": name,
                "rating": random.randint(3,5),
                "budget": random.randint(1,5),
                "type": "Tourist",
                "city": city,
                "state": "India"
            }

            places.append(place)

    time.sleep(1)

# Save dataset
with open("places.json", "w", encoding="utf-8") as f:
    json.dump(places, f, indent=4, ensure_ascii=False)

print("\nDataset created successfully!")
print("Total places collected:", len(places))