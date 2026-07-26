import requests
import json
from utils.paths import RAW_DATA_DIR

def extract_surface_area():
    url = "https://api.worldbank.org/v2/country/all/indicator/AG.SRF.TOTL.K2?format=json&per_page=30000"

    response = requests.get(url)
    response.raise_for_status()  # Error handling
    data = response.json()

    output_file = RAW_DATA_DIR / "surface_area_raw.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"Data saved to:\n{output_file}")

if __name__ == "__main__":
    extract_surface_area()