from database.connection import engine
from utils.paths import CLEANED_DATA_DIR
import pandas as pd
from sqlalchemy import MetaData, Table
from sqlalchemy.dialects.postgresql import insert

def load_population():
    countries_file = CLEANED_DATA_DIR / "countries.csv"
    population_file = CLEANED_DATA_DIR / "population.csv"

    countries_df = pd.read_csv(countries_file)
    population_df = pd.read_csv(population_file)

    records_countries = countries_df.to_dict(orient="records")
    records_population = population_df.to_dict(orient="records")

    metadata = MetaData()

    countries_table = Table(
        "countries",
        metadata,
        autoload_with=engine
    )

    countries_stmt = insert(countries_table).values(records_countries)
    countries_stmt = countries_stmt.on_conflict_do_nothing(
        index_elements=["iso3"]
    )

    population_table = Table(
        "population",
        metadata,
        autoload_with=engine
    )

    population_stmt = insert(population_table).values(records_population)
    population_stmt = population_stmt.on_conflict_do_nothing(
        index_elements=["iso3", "year"]
    )

    with engine.begin() as conn:
        conn.execute(countries_stmt)
        conn.execute(population_stmt)

if __name__ == "__main__":
    load_population()