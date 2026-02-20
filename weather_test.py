import requests

API_KEY = "dd3566a5bf56f8c2913ff0819001353b"

url = f"https://api.openweathermap.org/data/2.5/weather?q=Delhi,IN&appid={API_KEY}&units=metric"

response = requests.get(url)

print("Status:", response.status_code)
print(response.json())