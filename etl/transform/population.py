import pandas as pd
import json

with open("data/raw/population_raw.json", "r", encoding="utf-8") as file:
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

df.to_csv("data/cleaned/population_cleaned.csv",
          index=False)

print("\nCleaned data saved!")