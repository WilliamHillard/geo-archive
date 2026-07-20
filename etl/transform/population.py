import pandas as pd
import json
from utils.paths import RAW_DATA_DIR, CLEANED_DATA_DIR

input_file = RAW_DATA_DIR / "population_raw.json"

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
            "country": row["country"]["value"],
            "year": row["date"],
            "population": row["value"]
        }
    )

df = pd.DataFrame(cleaned_data)

# Remove rows without population
df = df.dropna(subset=["population"])

# Convert datatypes
df["year"] = df["year"].astype(int)
df["population"] = df["population"].astype(int)

print(df.head())
print(df.info())

output_file = CLEANED_DATA_DIR / "population_cleaned.csv"
df.to_csv(output_file, index=False)

print(f"\nCleaned data saved to:\n{output_file}")