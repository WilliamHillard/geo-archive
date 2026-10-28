import os
import re
import time
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from sqlalchemy import create_engine, text

# 1. Page Configuration
st.set_page_config(
    page_title="GeoArchive AI - Natural Language Query",
    page_icon="🌍",
    layout="wide",
)

# Load environment variables
load_dotenv()

# Initialize OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

1. `latest_country_statistics` (DEFAULT snapshot view for country stats/rankings/comparisons):
   Columns: "ISO3", "Country", "Income level", "Population year", "Population", "GDP year", "GDP", 
   "Internet users year", "Internet users (%)", "Life expectancy year", "Life expectancy", 
   "Inflation year", "Inflation", "Urban population year", "Urban population", 
   "Net migration year", "Net migration", "Unemployment year", "Unemployment"

2. `static_country_statistics` (Geographical details, Capital cities, & Region mappings):
   Columns: "ISO3", "Country", "Capital city", "Region", "Longitude", "Latitude", "Surface area (km²)"

3. `economic_statistics` (Time series data over years - ONLY use for historical year trends):
   Columns: "ISO3", "Country", "Region", "Year", "GDP", "Inflation", "Unemployment"

4. `social_statistics` (Time series data over years - ONLY use for historical year trends):
   Columns: "ISO3", "Country", "Region", "Income level", "Year", "Asylum seekers", 
   "Intentional homicides", "Internet users", "Life expectancy", "Literacy rate", "University enrollment"

5. `demographic_statistics` (Time series data over years - ONLY use for historical year trends):
   Columns: "ISO3", "Country", "Region", "Year", "Population", "Net migration", "Urban population"

CRITICAL SQL SYNTAX & JOIN RULES:
- `latest_country_statistics` DOES NOT contain a "Region" column! To filter `latest_country_statistics` by Region or Capital city, you MUST JOIN `static_country_statistics` ON "ISO3".
- EVERY column name MUST be enclosed in double quotes (e.g. "Country", "Capital city", "Life expectancy", "GDP").
- ALWAYS use table aliases (e.g. `latest_country_statistics l`, `static_country_statistics s`) and attach double-quoted columns to the alias (e.g. `s."Country"`, `s."Capital city"`, `l."Life expectancy"`).
- Filter text matching case-insensitively using `ILIKE '%pattern%'`.
- If user asks for 'South America' or 'Latin America', filter using `s."Region" ILIKE '%Latin America%'`.
- Return ONLY valid raw SQL query text without markdown backticks or explanations.

EXAMPLES:

Question: Compare life expectancy in South America.
SQL:
SELECT l."Country", l."Life expectancy"
FROM latest_country_statistics l
JOIN static_country_statistics s ON l."ISO3" = s."ISO3"
WHERE s."Region" ILIKE '%Latin America%' AND l."Life expectancy" IS NOT NULL
ORDER BY l."Life expectancy" DESC;

Question: What is every country with a capital city starting with C?
SQL:
SELECT "Country", "Capital city"
FROM static_country_statistics
WHERE "Capital city" ILIKE 'C%'
ORDER BY "Country";
"""


def clean_sql_output(raw_sql: str) -> str:
    """Removes any markdown code block formatting if present."""
    cleaned = re.sub(r"```sql\s*", "", raw_sql, flags=re.IGNORECASE)
    cleaned = re.sub(r"```\s*", "", cleaned)
    return cleaned.strip()


@st.cache_data(ttl=3600)
def generate_sql(user_question: str) -> str:
    """Sends user prompt to OpenAI gpt-4o-mini."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"User Question: {user_question}"},
        ],
        temperature=0.0,
    )
    raw_sql = response.choices[0].message.content
    return clean_sql_output(raw_sql)


def auto_generate_chart(df: pd.DataFrame):
    """Detects structure of returned DataFrame and renders appropriate Plotly charts."""
    if df.empty or len(df.columns) < 2:
        return

    columns = list(df.columns)
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    cat_col = None
    if "Country" in columns:
        cat_col = "Country"
    elif "Region" in columns:
        cat_col = "Region"
    elif len(categorical_cols) > 0:
        cat_col = categorical_cols[0]

    # Case A: Time series data (contains "Year" column)
    if "Year" in columns and len(numeric_cols) > 0:
        metrics = [col for col in numeric_cols if col != "Year"]
        if metrics:
            fig = px.line(
                df,
                x="Year",
                y=metrics,
                color=cat_col,
                title=f"{', '.join(metrics)} Over Time",
                markers=True,
            )
            st.plotly_chart(fig, use_container_width=True)

    # Case B: Categorical comparisons
    elif cat_col and len(numeric_cols) > 0:
        if len(numeric_cols) == 1:
            metric = numeric_cols[0]
            fig = px.bar(
                df,
                x=cat_col,
                y=metric,
                title=f"{metric} by {cat_col}",
                color=metric,
                color_continuous_scale="Viridis",
            )
            st.plotly_chart(fig, use_container_width=True)

        elif len(numeric_cols) == 2:
            m1, m2 = numeric_cols[0], numeric_cols[1]
            tab1, tab2 = st.tabs(["🔴 Scatter Plot (Correlation)", "📊 Separate Bar Charts"])

            with tab1:
                fig_scatter = px.scatter(
                    df,
                    x=m1,
                    y=m2,
                    color=cat_col,
                    title=f"{m1} vs. {m2}",
                    hover_name=cat_col,
                )
                fig_scatter.update_traces(marker=dict(size=12))
                st.plotly_chart(fig_scatter, use_container_width=True)

            with tab2:
                for metric in numeric_cols:
                    fig_bar = px.bar(
                        df,
                        x=cat_col,
                        y=metric,
                        title=f"{metric} by {cat_col}",
                        color=cat_col,
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)

        else:
            tab1, tab2 = st.tabs(["🔴 Scatter / Dot Plot", "📊 Separate Bar Charts"])

            with tab1:
                col_x, col_y = st.columns(2)
                x_metric = col_x.selectbox("Select X-axis metric:", numeric_cols, index=0)
                y_metric = col_y.selectbox("Select Y-axis metric:", numeric_cols, index=min(1, len(numeric_cols) - 1))

                fig_scatter = px.scatter(
                    df,
                    x=x_metric,
                    y=y_metric,
                    color=cat_col,
                    title=f"{x_metric} vs. {y_metric}",
                    hover_name=cat_col,
                )
                fig_scatter.update_traces(marker=dict(size=12))
                st.plotly_chart(fig_scatter, use_container_width=True)

            with tab2:
                for metric in numeric_cols:
                    fig_bar = px.bar(
                        df,
                        x=cat_col,
                        y=metric,
                        title=f"{metric} by {cat_col}",
                        color=cat_col,
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)


# --- HEADER UI ---
st.title("🌍 GeoArchive AI Query Engine")
st.markdown(
    "Type a natural language query to translate it into **SQL**, fetch live global indicators from **PostgreSQL**, and display interactive **Plotly charts**."
)

# --- SIDEBAR UI ---
st.sidebar.header("💡 Try Asking:")
st.sidebar.markdown(
    """
- *What are the top 5 countries by GDP in the latest data?*
- *Show Sweden's GDP and inflation trends over time.*
- *Compare life expectancy and GDP in South America.*
- *Which countries have the highest unemployment rate?*
"""
)

with st.sidebar.expander("📊 Available Data Parameters", expanded=False):
    st.markdown(
        """
    **📈 Economic Indicators**
    - **GDP**
    - **Inflation** (%)
    - **Unemployment** (%)

    **👥 Demographic Indicators**
    - **Population**
    - **Urban Population**
    - **Net Migration**

    **🎓 Social & Development**
    - **Life Expectancy** (Years)
    - **Literacy Rate** (%)
    - **Internet Users** (%)
    - **University Enrollment**
    - **Asylum Seekers**
    - **Intentional Homicides**

    **🌍 Regional & Metadata**
    - **Regions:** *Latin America & Caribbean, Europe & Central Asia, Sub-Saharan Africa, East Asia & Pacific, Middle East & North Africa, North America, South Asia*
    - **Income Levels:** *High income, Upper middle income, Lower middle income, Low income*
    - **Geography:** *Capital city, Coordinates, Surface area (km²)*
    """
    )

# --- USER INPUT ---
user_question = st.text_input(
    "Ask a question about global stats:",
    placeholder="e.g. Compare life expectancy and GDP in South America",
)

if user_question:
    # 1. Measure OpenAI Speed
    start_api_time = time.time()
    sql_query = None
    with st.spinner("🤖 OpenAI is generating SQL query..."):
        try:
            sql_query = generate_sql(user_question)
            api_duration = time.time() - start_api_time
        except Exception as e:
            st.error(f"Error generating SQL: {e}")

    if sql_query:
        with st.expander(f"🔍 View Generated SQL Query (AI Time: {api_duration:.2f}s)", expanded=False):
            st.code(sql_query, language="sql")

        # 2. Measure PostgreSQL Speed
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