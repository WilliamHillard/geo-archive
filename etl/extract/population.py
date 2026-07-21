import requests
import json
from utils.paths import RAW_DATA_DIR
def extract_population():
    url = "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json&per_page=30000"

    response = requests.get(url)
    response.raise_for_status() # Error handling
    data = response.json()

    output_file = RAW_DATA_DIR / "population_raw.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"Population data saved to:\n{output_file}")

if __name__ == "__main__":
    extract_population()