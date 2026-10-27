import os
import re
import pandas as pd
from dotenv import load_dotenv
from google import genai
from database.connection import engine

# Load environment variables
load_dotenv()

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Database Schema context for system prompt
SYSTEM_PROMPT = """
You are a PostgreSQL expert data analyst. Translate natural language user questions into executable SQL queries.

You must only query from these 5 database views:

1. `latest_country_statistics` (Snapshot of latest metrics per country):
   Columns: "ISO3", "Country", "Income level", "Population year", "Population", "GDP year", "GDP", 
   "Internet users year", "Internet users (%)", "Life expectancy year", "Life expectancy", 
   "Inflation year", "Inflation", "Urban population year", "Urban population", 
   "Net migration year", "Net migration", "Unemployment year", "Unemployment"

2. `economic_statistics` (Time series data over years):
   Columns: "ISO3", "Country", "Region", "Year", "GDP", "Inflation", "Unemployment"

3. `social_statistics` (Time series data over years):
   Columns: "ISO3", "Country", "Region", "Income level", "Year", "Asylum seekers", 
   "Intentional homicides", "Internet users", "Life expectancy", "Literacy rate", "University enrollment"

4. `demographic_statistics` (Time series data over years):
   Columns: "ISO3", "Country", "Region", "Year", "Population", "Net migration", "Urban population"

5. `static_country_statistics` (Static country geographical details):
   Columns: "ISO3", "Country", "Capital city", "Region", "Longitude", "Latitude", "Surface area (km²)"

IMPORTANT RULES:
- Column names are case-sensitive and must be enclosed in double quotes (e.g. "Country", "GDP", "Year").
- Table/view names are lowercase without quotes (e.g. economic_statistics).
- Return ONLY valid raw SQL query text. Do NOT wrap it in markdown code blocks (no ```sql or ```), and do NOT add explanatory text.
"""


def clean_sql_output(raw_sql: str) -> str:
    """Removes any markdown code block formatting if present."""
    cleaned = re.sub(r"```sql\s*", "", raw_sql, flags=re.IGNORECASE)
    cleaned = re.sub(r"```\s*", "", cleaned)
    return cleaned.strip()

def generate_sql(user_question: str) -> str:
    """Sends user prompt and schema to Gemini to generate SQL."""
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=f"{SYSTEM_PROMPT}\n\nUser Question: {user_question}",
    )
    return clean_sql_output(response.text)

def run_query(user_question: str):
    """Translates question to SQL, executes against PostgreSQL, and prints DataFrame."""
    print(f"\n--- Question: '{user_question}' ---")
    sql = generate_sql(user_question)
    print(f"\nGenerated SQL:\n{sql}\n")

    try:
        df = pd.read_sql(sql, engine)
        print("Query Results:")
        print(df)
        return df
    except Exception as e:
        print(f"Error executing query: {e}")
        return None

if __name__ == "__main__":
    # Test queries
    run_query("What are the top 5 countries by GDP in the latest data?")
    run_query("Show Sweden's GDP and inflation trends over time.")