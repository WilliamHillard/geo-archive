from database.connection import engine
from utils.paths import CLEANED_DATA_DIR
import pandas as pd

def load_population():
    countries_file = CLEANED_DATA_DIR / "countries.csv"
    population_file = CLEANED_DATA_DIR / "population.csv"

    countries_df = pd.read_csv(countries_file)
    population_df = pd.read_csv(population_file)

    countries_df.to_sql(
        "countries",
        engine,
        if_exists="append",
        index=False
    )

    population_df.to_sql(
        "population",
        engine,
        if_exists="append",
        index=False
    )

if __name__ == "__main__":
    load_population()