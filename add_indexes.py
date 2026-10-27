from sqlalchemy import text
from database.connection import engine

indexes_sql = """
CREATE INDEX IF NOT EXISTS idx_gdp_iso3_year ON gdp(iso3, year DESC);
CREATE INDEX IF NOT EXISTS idx_pop_iso3_year ON population(iso3, year DESC);
CREATE INDEX IF NOT EXISTS idx_life_iso3_year ON life_expectancy(iso3, year DESC);
CREATE INDEX IF NOT EXISTS idx_inf_iso3_year ON inflation(iso3, year DESC);
CREATE INDEX IF NOT EXISTS idx_unemp_iso3_year ON unemployment(iso3, year DESC);
CREATE INDEX IF NOT EXISTS idx_urb_iso3_year ON urban_population(iso3, year DESC);
CREATE INDEX IF NOT EXISTS idx_net_iso3_year ON net_migration(iso3, year DESC);
CREATE INDEX IF NOT EXISTS idx_surf_iso3_year ON surface_area(iso3, year DESC);
"""

print("Creating indexes on PostgreSQL tables...")
with engine.connect() as conn:
    conn.execute(text(indexes_sql))
    conn.commit()

print("✅ All database indexes created successfully!")