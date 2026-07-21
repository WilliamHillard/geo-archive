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
            "country_name": row["country"]["value"],
            "year": row["date"],
            "population": row["value"]
        }
    )

df = pd.DataFrame(cleaned_data)

# Remove rows without population
df = df.dropna(subset=["population"])
df = df[df["iso3"].str.len() == 3]

# Convert datatypes
df["year"] = df["year"].astype(int)
df["population"] = df["population"].astype(int)

df_countries = (
    df[["iso3", "country_name"]]
    .drop_duplicates()
    .sort_values("iso3")
)

print(df_countries["iso3"] == "")

df_population = df[["iso3", "year", "population"]]

output_countries = CLEANED_DATA_DIR / "countries.csv"
df_countries.to_csv(output_countries, index=False)

output_population = CLEANED_DATA_DIR / "population.csv"
df_population.to_csv(output_population, index=False)

print(f"\nCleaned data saved!")