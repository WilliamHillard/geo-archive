import requests

url = "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json&per_page=30000"

response = requests.get(url)

print(response.status_code)

data = response.json()

print(type(data))
print(len(data))