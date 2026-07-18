import requests
import json

url = "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json&per_page=30000"

response = requests.get(url)

data = response.json()

with open("data/raw/population_raw.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)

print("Population data saved!")