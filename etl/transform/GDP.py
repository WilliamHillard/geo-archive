import pandas as pd
import json
from utils.paths import RAW_DATA_DIR, CLEANED_DATA_DIR

def transform_gdp():
    input_file = RAW_DATA_DIR / "gdp_raw.json"

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
                "gdp": row["value"]
            }
        )
    df = pd.DataFrame(cleaned_data)

    # Remove rows without population
    df = df.dropna(subset=["gdp"]) # 2745 rows
    df = df[df["iso3"].str.len() == 3] # 330 rows

    # Convert datatypes
    df["year"] = df["year"].astype(int)
    df["gdp"] = df["gdp"].astype(float)

    output = CLEANED_DATA_DIR / "gdp.csv"
    df.to_csv(output, index=False)

    print(f"\nCleaned data saved!")

if __name__ == "__main__":
    transform_gdp()