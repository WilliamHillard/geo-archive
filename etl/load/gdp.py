from database.connection import engine
from utils.paths import CLEANED_DATA_DIR
import pandas as pd
from sqlalchemy import MetaData, Table
from sqlalchemy.dialects.postgresql import insert

def load_gdp():
    file = CLEANED_DATA_DIR / "gdp.csv"

    df = pd.read_csv(file)

    records = df.to_dict(orient="records")

    metadata = MetaData()

    table = Table(
        "gdp",
        metadata,
        autoload_with=engine
    )

    stmt = insert(table).values(records)
    stmt = stmt.on_conflict_do_nothing(
        index_elements=["iso3", "year"]
    )

    with engine.begin() as conn:
        conn.execute(stmt)

if __name__ == "__main__":
    load_gdp()