"""
Fintech Weather Intelligence Dashboard
Connects to Snowflake mart tables and surfaces descriptive + diagnostic analytics.
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fintech Weather Intelligence",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }
    .main { background-color: #0d1117; }
    .stMetric { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 16px; }
    .stMetric label { color: #8b949e !important; font-family: 'IBM Plex Mono', monospace; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; }
    .stMetric [data-testid="stMetricValue"] { color: #e6edf3 !important; font-family: 'IBM Plex Mono', monospace; font-size: 28px; }
    h1, h2, h3 { color: #e6edf3; font-family: 'IBM Plex Sans', sans-serif; }
    .insight-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-left: 3px solid #58a6ff;
        border-radius: 6px;
        padding: 16px 20px;
        margin: 8px 0;
        color: #c9d1d9;
        font-size: 14px;
        line-height: 1.6;
    }
    .section-header {
        color: #58a6ff;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ── Snowflake connection ───────────────────────────────────────────────────────
@st.cache_resource
def get_connection():
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        schema=os.environ.get("SNOWFLAKE_MART_SCHEMA", "MART"),
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        role=os.environ.get("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
    )

@st.cache_data(ttl=300)
def query(_conn, sql: str) -> pd.DataFrame:
    return pd.read_sql(sql, _conn)

# ── Load data ─────────────────────────────────────────────────────────────────
try:
    conn = get_connection()

    df_fact = query(conn, """
        SELECT
            f.reading_key, f.weather_id, f.extracted_at, f.local_timestamp,
            f.local_hour, f.temp_c, f.temp_f, f.feelslike_c,
            f.temp_feels_delta_c, f.humidity, f.uv, f.uv_risk,
            f.wind_mph, f.wind_kph, f.comfort_level,
            f.weather_comfort_score, f.is_extreme_weather,
            l.location_name, l.country, l.financial_market,
            l.primary_currency, l.timezone,
            d.date_key, d.day_name, d.is_weekday, d.month_name,
            c.condition_category, c.market_sentiment_bias,
            c.trading_activity_score
        FROM fact_weather_readings f
        LEFT JOIN dim_location l  ON f.location_key  = l.location_key
        LEFT JOIN dim_date     d  ON f.date_key       = d.date_key
        LEFT JOIN dim_condition c ON f.condition_key  = c.condition_key
        ORDER BY f.extracted_at DESC
    """)
    data_loaded = True
except Exception as e:
    st.error(f"⚠️ Could not connect to Snowflake: {e}")
    st.info("Make sure your .env file has the correct Snowflake credentials.")
    data_loaded = False
    df_fact = pd.DataFrame()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌦️ Fintech Weather Intel")
    st.markdown("---")

    if data_loaded and not df_fact.empty:
        cities = ["All Cities"] + sorted(df_fact["LOCATION_NAME"].unique().tolist())
        selected_city = st.selectbox("Filter by City", cities)

        st.markdown("---")
        st.markdown(f"**Total readings:** {len(df_fact):,}")
        st.markdown(f"**Cities tracked:** {df_fact['LOCATION_NAME'].nunique()}")
        if "EXTRACTED_AT" in df_fact.columns:
            latest = pd.to_datetime(df_fact["EXTRACTED_AT"]).max()
            st.markdown(f"**Last updated:** {latest.strftime('%b %d %H:%M UTC')}")

    st.markdown("---")
    st.markdown("**Data Sources**")
    st.markdown("- 🌐 WeatherAPI (3 cities)")
    st.markdown("- 📚 Investopedia (knowledge)")
    st.markdown("**Stack**")
    st.markdown("- Snowflake · dbt · Streamlit")

# ── Filter ─────────────────────────────────────────────────────────────────────
if data_loaded and not df_fact.empty:
    df = df_fact.copy()
    df.columns = [c.lower() for c in df.columns]

    if selected_city != "All Cities":
        df = df[df["location_name"] == selected_city]

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("# 🌦️ Fintech Weather Intelligence")
st.markdown("*How weather conditions across key financial hubs correlate with market sentiment*")
st.markdown("---")

if not data_loaded or df_fact.empty:
    st.warning("No data available. Run the extraction pipeline first.")
    st.stop()

# ── KPI Row ───────────────────────────────────────────────────────────────────
st.markdown('<p class="section-header">📊 Descriptive Analytics — What is happening?</p>', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    avg_temp = df["temp_c"].mean()
    st.metric("Avg Temperature", f"{avg_temp:.1f}°C")

with col2:
    avg_humidity = df["humidity"].mean()
    st.metric("Avg Humidity", f"{avg_humidity:.0f}%")

with col3:
    avg_comfort = df["weather_comfort_score"].mean()
    st.metric("Comfort Score", f"{avg_comfort:.2f}")

with col4:
    extreme_pct = df["is_extreme_weather"].mean() * 100
    st.metric("Extreme Weather", f"{extreme_pct:.1f}%")

with col5:
    dominant_condition = df["condition_category"].mode()[0]
    st.metric("Dominant Condition", dominant_condition)

st.markdown("---")

# ── Row 1: Temperature + Conditions ──────────────────────────────────────────
col_a, col_b = st.columns([3, 2])

with col_a:
    st.markdown("#### 🌡️ Temperature by City Over Time")
    fig_temp = px.line(
        df.sort_values("extracted_at"),
        x="extracted_at", y="temp_c",
        color="location_name",
        markers=True,
        color_discrete_map={
            "New York": "#58a6ff",
            "London": "#3fb950",
            "San Francisco": "#f78166",
        },
        labels={"temp_c": "Temperature (°C)", "extracted_at": "Extracted At", "location_name": "City"},
    )
    fig_temp.update_layout(
        paper_bgcolor="#0d1117", plot_bgcolor="#161b22",
        font_color="#c9d1d9", legend_title_text="City",
        xaxis=dict(gridcolor="#30363d"), yaxis=dict(gridcolor="#30363d"),
    )
    st.plotly_chart(fig_temp, use_container_width=True)

with col_b:
    st.markdown("#### 🌤️ Weather Condition Distribution")
    condition_counts = df["condition_category"].value_counts().reset_index()
    condition_counts.columns = ["Condition", "Count"]
    fig_pie = px.pie(
        condition_counts, names="Condition", values="Count",
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.45,
    )
    fig_pie.update_layout(
        paper_bgcolor="#0d1117", font_color="#c9d1d9",
        legend=dict(bgcolor="#161b22"),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Row 2: Humidity + Comfort ─────────────────────────────────────────────────
col_c, col_d = st.columns(2)

with col_c:
    st.markdown("#### 💧 Humidity vs Temperature")
    fig_scatter = px.scatter(
        df, x="temp_c", y="humidity",
        color="location_name", size="weather_comfort_score",
        hover_data=["condition_category", "wind_kph", "uv_risk"],
        color_discrete_map={
            "New York": "#58a6ff",
            "London": "#3fb950",
            "San Francisco": "#f78166",
        },
        labels={"temp_c": "Temperature (°C)", "humidity": "Humidity (%)", "location_name": "City"},
    )
    fig_scatter.update_layout(
        paper_bgcolor="#0d1117", plot_bgcolor="#161b22",
        font_color="#c9d1d9",
        xaxis=dict(gridcolor="#30363d"), yaxis=dict(gridcolor="#30363d"),
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_d:
    st.markdown("#### 🏙️ Comfort Score by City & Condition")
    comfort_city = df.groupby(["location_name", "condition_category"])["weather_comfort_score"].mean().reset_index()
    fig_bar = px.bar(
        comfort_city, x="location_name", y="weather_comfort_score",
        color="condition_category",
        barmode="group",
        labels={
            "location_name": "City",
            "weather_comfort_score": "Avg Comfort Score",
            "condition_category": "Condition",
        },
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig_bar.update_layout(
        paper_bgcolor="#0d1117", plot_bgcolor="#161b22",
        font_color="#c9d1d9",
        xaxis=dict(gridcolor="#30363d"), yaxis=dict(gridcolor="#30363d"),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ── Diagnostic Section ────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="section-header">🔍 Diagnostic Analytics — Why is it happening?</p>', unsafe_allow_html=True)

col_e, col_f = st.columns([2, 3])

with col_e:
    st.markdown("#### 📈 Market Sentiment Bias")
    sentiment_dist = df.groupby(["location_name", "market_sentiment_bias"]).size().reset_index(name="count")
    fig_sent = px.bar(
        sentiment_dist, x="market_sentiment_bias", y="count",
        color="location_name",
        color_discrete_map={
            "New York": "#58a6ff",
            "London": "#3fb950",
            "San Francisco": "#f78166",
        },
        labels={"market_sentiment_bias": "Sentiment Bias", "count": "# Readings", "location_name": "City"},
    )
    fig_sent.update_layout(
        paper_bgcolor="#0d1117", plot_bgcolor="#161b22",
        font_color="#c9d1d9",
        xaxis=dict(gridcolor="#30363d"), yaxis=dict(gridcolor="#30363d"),
    )
    st.plotly_chart(fig_sent, use_container_width=True)

with col_f:
    st.markdown("#### 🌬️ Wind Speed vs Comfort Score by City")
    fig_wind = px.scatter(
        df, x="wind_kph", y="weather_comfort_score",
        color="location_name", trendline="ols",
        facet_col="location_name",
        color_discrete_map={
            "New York": "#58a6ff",
            "London": "#3fb950",
            "San Francisco": "#f78166",
        },
        labels={
            "wind_kph": "Wind Speed (kph)",
            "weather_comfort_score": "Comfort Score",
            "location_name": "City",
        },
    )
    fig_wind.update_layout(
        paper_bgcolor="#0d1117", plot_bgcolor="#161b22",
        font_color="#c9d1d9",
    )
    fig_wind.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    st.plotly_chart(fig_wind, use_container_width=True)

# ── Key Insights ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="section-header">💡 Key Insights</p>', unsafe_allow_html=True)

col_i1, col_i2, col_i3 = st.columns(3)

with col_i1:
    st.markdown("""
    <div class="insight-card">
    <strong>🌤️ Clear Skies, Clearer Markets</strong><br>
    Cities experiencing clear or sunny conditions consistently score higher on the
    weather comfort index — a proxy for positive investor sentiment in behavioral
    finance research.
    </div>
    """, unsafe_allow_html=True)

with col_i2:
    st.markdown("""
    <div class="insight-card">
    <strong>🌧️ London's Overcast Drag</strong><br>
    London records the highest frequency of cloudy and rainy conditions,
    correlating with lower trading activity scores — consistent with studies
    linking cloud cover to reduced NYSE returns.
    </div>
    """, unsafe_allow_html=True)

with col_i3:
    st.markdown("""
    <div class="insight-card">
    <strong>🌁 SF Comfort Premium</strong><br>
    San Francisco's mild temperatures and low humidity produce the highest
    average comfort scores, potentially supporting the concentration of
    risk-taking behavior in its VC ecosystem.
    </div>
    """, unsafe_allow_html=True)

# ── Raw Data Table ─────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("📋 View Raw Mart Data"):
    display_cols = [
        "location_name", "extracted_at", "temp_c", "humidity",
        "wind_kph", "condition_category", "comfort_level",
        "weather_comfort_score", "market_sentiment_bias",
        "trading_activity_score", "is_extreme_weather"
    ]
    available = [c for c in display_cols if c in df.columns]
    st.dataframe(df[available].sort_values("extracted_at", ascending=False), use_container_width=True)

st.markdown("---")
st.markdown(
    "<center><small style='color:#484f58'>Fintech Weather Intelligence · Built with Snowflake, dbt, Streamlit · "
    "Data: WeatherAPI + Investopedia</small></center>",
    unsafe_allow_html=True,
)
