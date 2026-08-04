import pandas as pd
import json
from utils.paths import RAW_DATA_DIR, CLEANED_DATA_DIR

def transform_university_enrollment():
    input_file = RAW_DATA_DIR / "university_enrollment_raw.json"

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
                "university_enrollment": row["value"]
            }
        )
    df = pd.DataFrame(cleaned_data)

    df = df.dropna(subset=["university_enrollment"])
    valid_countries = pd.read_csv(
        CLEANED_DATA_DIR / "countries.csv",
        keep_default_na=False
    )

    df = df[df["iso3"].isin(valid_countries["iso3"])]

    # Convert datatypes
    df["year"] = df["year"].astype(int)
    df["university_enrollment"] = df["university_enrollment"].astype(float)

    output = CLEANED_DATA_DIR / "university_enrollment.csv"
    df.to_csv(output, index=False)

    print(f"\nCleaned university enrollment data saved!")

if __name__ == "__main__":
    transform_university_enrollment()