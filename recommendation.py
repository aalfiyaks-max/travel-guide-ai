import json
import random


def load_places():
    with open("places.json", "r", encoding="utf-8") as file:
        return json.load(file)


def recommend_places(budget, limit=5):

    places = load_places()

    filtered = [place for place in places if place["budget"] <= budget]

    if len(filtered) > limit:
        return random.sample(filtered, limit)

    return filtered


def recommend_by_city(city, budget, limit=5):

    places = load_places()

    filtered = [
        place for place in places
        if place["budget"] <= budget and place["city"].lower() == city.lower()
    ]

    if len(filtered) > limit:
        return random.sample(filtered, limit)

    return filtered


# Test
if __name__ == "__main__":
    print(recommend_places(3))