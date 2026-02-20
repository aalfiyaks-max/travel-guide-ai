import json
from sklearn.neighbors import NearestNeighbors
import numpy as np

# Load place data
with open("places.json") as f:
    data = json.load(f)

# Convert to ML format
X = []
names = []

for place in data:
    X.append([place["rating"], place["budget"]])
    names.append(place["name"])

model = NearestNeighbors(n_neighbors=3)
model.fit(X)

def recommend(rating, budget):
    distances, indices = model.kneighbors([[rating, budget]])
    results = []
    
    for i in indices[0]:
        results.append(names[i])
    
    return results