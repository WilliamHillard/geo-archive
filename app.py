import os
import re
import time
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from sqlalchemy import create_engine, text

# 1. Page Configuration
st.set_page_config(
    page_title="GeoArchive AI - Natural Language Query",
    page_icon="🌍",
    layout="wide",
)

# Load environment variables
load_dotenv()

# Initialize Groq Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Cache Database Engine
@st.cache_resource
def get_db_engine():
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    return create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

engine = get_db_engine()

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

CRITICAL DATA MATCHING RULES:
- Regions strictly use World Bank categories:
  'Latin America & Caribbean', 'Europe & Central Asia', 'Sub-Saharan Africa', 
  'East Asia & Pacific', 'Middle East & North Africa', 'North America', 'South Asia'.
- If user asks for 'South America' or 'Latin America', filter strictly using `ILIKE '%Latin America%'`. Never use '%South%' as it incorrectly includes 'South Asia'.
- ALWAYS use case-insensitive wildcard matching (`ILIKE '%pattern%'`) for text filtering on Region or Country.
- Column names are case-sensitive and must be enclosed in double quotes (e.g. "Country", "GDP", "Year").
- Table/view names are lowercase without quotes (e.g. latest_country_statistics).
- Return ONLY valid raw SQL query text without markdown backticks or explanations.
"""


def clean_sql_output(raw_sql: str) -> str:
    """Removes any markdown code block formatting if present."""
    cleaned = re.sub(r"```sql\s*", "", raw_sql, flags=re.IGNORECASE)
    cleaned = re.sub(r"```\s*", "", cleaned)
    return cleaned.strip()


@st.cache_data(ttl=3600)
def get_active_groq_model() -> str:
    """Dynamically fetches active models from Groq to prevent 404 errors."""
    try:
        models = client.models.list()
        active_ids = [m.id for m in models.data]
        for preferred in ["llama-3.1-8b-instant", "llama3-70b-8192", "llama-3.3-70b-versatile"]:
            if preferred in active_ids:
                return preferred
        return active_ids[0] if active_ids else "llama-3.1-8b-instant"
    except Exception:
        return "llama-3.1-8b-instant"


@st.cache_data(ttl=3600)
def generate_sql(user_question: str) -> str:
    """Sends user prompt to Groq API using an auto-detected active model."""
    model_id = get_active_groq_model()
    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"User Question: {user_question}"},
        ],
        temperature=0.0,
    )
    # Specified [0] index on the choices list
    raw_sql = response.choices[0].message.content
    return clean_sql_output(raw_sql)


def auto_generate_chart(df: pd.DataFrame):
    """Detects structure of returned DataFrame and renders a Plotly chart."""
    if df.empty or len(df.columns) < 2:
        return

    columns = list(df.columns)
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    # Case A: Time series data (contains "Year" column)
    if "Year" in columns and len(numeric_cols) > 0:
        metrics = [col for col in numeric_cols if col != "Year"]
        if metrics:
            color_col = "Country" if "Country" in columns else None
            fig = px.line(
                df,
                x="Year",
                y=metrics,
                color=color_col,
                title=f"{', '.join(metrics)} Over Time",
                markers=True,
            )
            st.plotly_chart(fig, use_container_width=True)

    # Case B: Categorical comparison (e.g., Country vs Metric)
    elif "Country" in columns and len(numeric_cols) > 0:
        fig = px.bar(
            df,
            x="Country",
            y=numeric_cols,
            barmode="group",
            title="Comparison by Country",
        )
        st.plotly_chart(fig, use_container_width=True)


# --- HEADER UI ---
st.title("🌍 GeoArchive AI Query Engine")
st.markdown(
    "Type a natural language query to translate it into **SQL**, fetch live global indicators from **PostgreSQL**, and display interactive **Plotly charts**."
)

# Sidebar with sample prompts
st.sidebar.header("💡 Try Asking:")
st.sidebar.markdown(
    """
- *What are the top 5 countries by GDP in the latest data?*
- *Show Sweden's GDP and inflation trends over time.*
- *Compare life expectancy in South America.*
- *Which countries have the highest unemployment rate?*
"""
)

# --- USER INPUT ---
user_question = st.text_input(
    "Ask a question about global stats:",
    placeholder="e.g. Compare life expectancy in South America",
)

if user_question:
    # 1. Measure Groq AI Speed
    start_api_time = time.time()
    sql_query = None
    with st.spinner("⚡ Groq AI is generating SQL query..."):
        try:
            sql_query = generate_sql(user_question)
            api_duration = time.time() - start_api_time
        except Exception as e:
            st.error(f"Error generating SQL: {e}")

    if sql_query:
        # Display Generated SQL
        with st.expander(f"🔍 View Generated SQL Query (AI Time: {api_duration:.2f}s)", expanded=False):
            st.code(sql_query, language="sql")

        # 2. Measure PostgreSQL Database Speed
        start_db_time = time.time()
        df = None
        with st.spinner("🐘 Executing SQL query on PostgreSQL..."):
            try:
                with engine.connect() as conn:
                    df = pd.read_sql(text(sql_query), conn)
                db_duration = time.time() - start_db_time
                st.caption(f"⚡ DB Query executed in {db_duration:.2f} seconds.")
            except Exception as e:
                st.error(f"Error executing database query: {e}")

        # 3. Display Results
        if df is not None:
            if df.empty:
                st.warning("Query executed successfully, but returned 0 results.")
            else:
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("📋 Query Results")
                    st.dataframe(df, use_container_width=True)

                with col2:
                    st.subheader("📊 Visualization")
                    auto_generate_chart(df)