import streamlit as st
import pandas as pd
import plotly.express as px
import json

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="India Crime Dashboard", layout="wide")

st.title("🚔 India Crime Dashboard")

# =========================
# LOAD ALL CSVs
# =========================
@st.cache_data
def load_data():
    df_master = pd.read_csv("ncrb_master_dataset.csv")
    df_total = pd.read_csv("ncrb_total_trends.csv")
    df_yoy = pd.read_csv("ncrb_yoy_changes.csv")
    df_trends = pd.read_csv("ncrb_crime_trends.csv")
    df_women = pd.read_csv("ncrb_women_analysis_2023.csv")

    return df_master, df_total, df_yoy, df_trends, df_women

df_master, df_total, df_yoy, df_trends, df_women = load_data()

# =========================
# SIDEBAR
# =========================
st.sidebar.header("Filters")

states = sorted(df_master['state'].unique())
crime_types = sorted(df_master['crime_type'].unique())

selected_states = st.sidebar.multiselect("States", states, default=states[:5])
selected_crime = st.sidebar.selectbox("Crime Type", crime_types)

filtered = df_master[
    (df_master['state'].isin(selected_states)) &
    (df_master['crime_type'] == selected_crime)
]

# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Trends",
    "🏆 State Ranking",
    "📊 YOY Growth",
    "📊 Crime Type Trends",
    "👩 Women Crime Analysis",
    "🗺️ Map"
])

# =========================
# TAB 1: TRENDS (MASTER)
# =========================
with tab1:
    st.subheader("Trend Analysis")

    fig = px.line(filtered, x='year', y='count', color='state', markers=True)
    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 2: STATE RANKING (TOTAL CSV)
# =========================
with tab2:
    st.subheader("Top States by Total Crime (2023)")

    df_2023 = df_total[df_total['year'] == 2023]

    fig = px.bar(df_2023.sort_values(by='total_crimes'),
                 x='total_crimes', y='state',
                 orientation='h', color='total_crimes')

    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 3: YOY (STATE LEVEL)
# =========================
with tab3:
    st.subheader("State Growth (2021–2023)")

    fig = px.bar(df_yoy.sort_values(by='pct_21_23'),
                 x='pct_21_23', y='state',
                 orientation='h', color='pct_21_23')

    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 4: CRIME TYPE TRENDS
# =========================
with tab4:
    st.subheader("Crime Type Growth")

    fig = px.bar(df_trends.sort_values(by='pct_21_23'),
                 x='pct_21_23', y='crime_type',
                 orientation='h', color='pct_21_23')

    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 5: WOMEN CRIME (VERY IMPORTANT)
# =========================
with tab5:
    st.subheader("Women Crime Analysis (2023)")

    fig = px.bar(df_women.sort_values(by='women_crime_percentage'),
                 x='women_crime_percentage', y='state',
                 orientation='h', color='women_crime_percentage')

    st.plotly_chart(fig, use_container_width=True)

    # Insight
    if not df_women.empty:
     top = df_women.sort_values(by='women_crime_percentage', ascending=False).iloc[0]
     st.warning(f"Highest Women Crime %: {top['state']} ({top['women_crime_percentage']:.2f}%)")
    else:
       st.error("No data available for Women Crime Analysis")
# =========================
# TAB 6: MAP
with tab6:
    st.subheader("🗺️ India Crime Map (2023)")

    # Load geojson
    with open("india_states.geojson") as f:
        geojson = json.load(f)

    # Filter data
    map_data = df_total[df_total['year'] == 2023].copy()

    # =========================
    # CLEAN STATE NAMES
    # =========================
    map_data['state'] = map_data['state'].str.strip().str.lower()

    # Geojson clean
    for feature in geojson["features"]:
        feature["properties"]["NAME_1"] = feature["properties"]["NAME_1"].strip().lower()

    # =========================
    # STATE NAME FIXES (VERY IMPORTANT)
    # =========================
    state_mapping = {
        "andaman & nicobar islands": "andaman and nicobar",
        "dadra & nagar haveli and daman & diu": "dadra and nagar haveli and daman and diu",
        "delhi": "nct of delhi",
        "odisha": "orissa",
        "jammu & kashmir": "jammu and kashmir",
        "ladakh": "ladakh"
    }

    map_data['state'] = map_data['state'].replace(state_mapping)

    # =========================
    # DEBUG (IMPORTANT)
    # =========================
    geo_states = set([f["properties"]["NAME_1"] for f in geojson["features"]])
    data_states = set(map_data['state'])

    missing = data_states - geo_states

    if len(missing) > 0:
        st.warning(f"Unmatched states: {missing}")

    # =========================
    # PLOT
    # =========================
    fig = px.choropleth(
        map_data,
        geojson=geojson,
        featureidkey="properties.NAME_1",
        locations="state",
        color="total_crimes",
        color_continuous_scale="Reds"
    )

    fig.update_geos(fitbounds="locations", visible=False)

    st.plotly_chart(fig, use_container_width=True)