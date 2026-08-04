import pandas as pd
import json
from utils.paths import RAW_DATA_DIR, CLEANED_DATA_DIR

def transform_asylum_seekers():
    input_file = RAW_DATA_DIR / "asylum_seekers_raw.json"

    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    # The World Bank API stores metadata in index 0
    # and the actual observations in index 1
    observations = data[1]

    cleaned_data = []

    for row in observations:
        cleaned_data.append(
            {
                "iso3": row["countryiso3code"],
                "year": row["date"],
                "asylum_seekers": row["value"]
            }
        )
    df = pd.DataFrame(cleaned_data)

    # Remove rows without population
    df = df.dropna(subset=["asylum_seekers"])
    valid_countries = pd.read_csv(
        CLEANED_DATA_DIR / "countries.csv",
        keep_default_na=False
    )

    df = df[df["iso3"].isin(valid_countries["iso3"])]

    # Convert datatypes
    df["year"] = df["year"].astype(int)
    df["asylum_seekers"] = df["asylum_seekers"].astype(int)

    output = CLEANED_DATA_DIR / "asylum_seekers.csv"
    df.to_csv(output, index=False)

    print(f"\nCleaned asylum seekers data saved!")

if __name__ == "__main__":
    transform_asylum_seekers()