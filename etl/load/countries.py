from database.connection import engine
from utils.paths import CLEANED_DATA_DIR
import pandas as pd
from sqlalchemy import MetaData, Table
from sqlalchemy.dialects.postgresql import insert

def load_countries():
    file = CLEANED_DATA_DIR / "countries.csv"

    df = pd.read_csv(file, keep_default_na=False)

    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")

    records = df.to_dict(orient="records")

    metadata = MetaData()

    table = Table(
        "countries",
        metadata,
        autoload_with=engine
    )

    stmt = insert(table).values(records)
    stmt = stmt.on_conflict_do_nothing(
        index_elements=["iso3"]
    )

    with engine.begin() as conn:
        conn.execute(stmt)

if __name__ == "__main__":
    load_countries()