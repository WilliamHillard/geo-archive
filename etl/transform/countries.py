import pandas as pd
import json
from utils.paths import RAW_DATA_DIR, CLEANED_DATA_DIR

def transform_countries():
    input_file = RAW_DATA_DIR / "countries_raw.json"

    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    # The World Bank API stores metadata in index 0
    # and the actual observations in index 1
    observations = data[1]

    cleaned_data = []

    for row in observations:
        cleaned_data.append(
            {
                "iso3": row["id"],
                "iso2": row["iso2Code"],
                "country_name": row["name"],
                "capital_city": row["capitalCity"],
                "region": row["region"]["value"],
                "longitude": row["longitude"],
                "latitude": row["latitude"],
                "income_level": row["incomeLevel"]["value"],
                "lending_type": row["lendingType"]["value"]
            }
        )
    df = pd.DataFrame(cleaned_data)

    df = df[df["region"] != "Aggregates"]
    df = df[df["iso3"].str.len() == 3]

    # Convert datatypes
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")

    output = CLEANED_DATA_DIR / "countries.csv"
    df.to_csv(output, index=False)

    print(f"\nCleaned countries data saved!")

if __name__ == "__main__":
    transform_countries()