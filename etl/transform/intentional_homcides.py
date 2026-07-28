import pandas as pd
import json
from utils.paths import RAW_DATA_DIR, CLEANED_DATA_DIR

def transform_intentional_homicides():
    input_file = RAW_DATA_DIR / "intentional_homicides_raw.json"

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
                "intentional_homicides": row["value"]
            }
        )
    df = pd.DataFrame(cleaned_data)

    # Remove rows without population
    df = df.dropna(subset=["intentional_homicides"])
    df = df[df["iso3"].str.len() == 3]

    # Convert datatypes
    df["year"] = df["year"].astype(int)
    df["intentional_homicides"] = df["intentional_homicides"].astype(float)

    output = CLEANED_DATA_DIR / "intentional_homicides.csv"
    df.to_csv(output, index=False)

    print(f"\nCleaned intentional homicides data saved!")

if __name__ == "__main__":
    transform_intentional_homicides()