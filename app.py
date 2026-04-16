import streamlit as st
import pandas as pd
import plotly.express as px
import json

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="India Crime Dashboard", layout="wide")

# =========================
# 🎨 GLASS UI
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🚔 India Crime Dashboard")

# =========================
# LOAD DATA
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
st.sidebar.header("📊 Filters")

states = sorted(df_master['state'].unique())
crime_types = sorted(df_master['crime_type'].unique())

selected_states = st.sidebar.multiselect("States", states, default=states[:5])
selected_crime = st.sidebar.selectbox("Crime Type", crime_types)

# 🔍 SEARCH
search_state = st.sidebar.text_input("🔍 Search State")

filtered = df_master[
    (df_master['state'].isin(selected_states)) &
    (df_master['crime_type'] == selected_crime)
]

if search_state:
    filtered = filtered[filtered['state'].str.contains(search_state.lower())]

# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Trends",
    "🏆 State Ranking",
    "📊 YOY Growth",
    "📊 Crime Type Trends",
    "👩 Women Crime",
    "🗺️ Map"
])

# =========================
# TAB 1: TRENDS
# =========================
with tab1:
    st.subheader("📈 Crime Trend Analysis")

    latest = filtered[filtered['year'] == 2023]['count'].sum()
    prev = filtered[filtered['year'] == 2021]['count'].sum()
    growth = ((latest - prev) / prev) * 100 if prev != 0 else 0

    c1, c2 = st.columns(2)
    c1.metric("Total Crimes (2023)", f"{int(latest):,}")
    c2.metric("Growth %", f"{growth:.2f}%")

    fig = px.line(filtered, x='year', y='count', color='state', markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(filtered, use_container_width=True)

# =========================
# TAB 2: STATE RANKING
# =========================
with tab2:
    st.subheader("🏆 State Ranking (2023)")

    df_2023 = df_total[df_total['year'] == 2023]

    view_option = st.radio("View", ["All", "Top 5", "Bottom 5"], horizontal=True)

    if view_option == "Top 5":
        df_display = df_2023.sort_values(by='total_crimes', ascending=False).head(5)
    elif view_option == "Bottom 5":
        df_display = df_2023.sort_values(by='total_crimes').head(5)
    else:
        df_display = df_2023

    top_state = df_2023.loc[df_2023['total_crimes'].idxmax()]
    total_sum = df_2023['total_crimes'].sum()

    c1, c2 = st.columns(2)
    c1.metric("🔴 Highest Crime State", top_state['state'])
    c2.metric("📊 Total Crimes", f"{int(total_sum):,}")

    fig = px.bar(
        df_display.sort_values(by='total_crimes'),
        x='total_crimes',
        y='state',
        orientation='h',
        color='total_crimes',
        text='total_crimes'
    )

    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df_display, use_container_width=True)

# =========================
# TAB 3: YOY
# =========================
with tab3:
    st.subheader("📊 Growth Analysis")

    min_growth = st.slider("Minimum % Growth", -100, 200, 0)

    filtered_yoy = df_yoy[df_yoy['pct_21_23'] >= min_growth]

    fig = px.bar(
        filtered_yoy.sort_values(by='pct_21_23'),
        x='pct_21_23',
        y='state',
        orientation='h',
        color='pct_21_23',
        text='pct_21_23'
    )

    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(filtered_yoy, use_container_width=True)

# =========================
# TAB 4: CRIME TYPE
# =========================
with tab4:
    st.subheader("📊 Crime Type Trends")

    top_n = st.slider("Top N Crimes", 5, 20, 10)

    filtered_trends = df_trends.sort_values(by='pct_21_23', ascending=False).head(top_n)

    fig = px.bar(
        filtered_trends,
        x='pct_21_23',
        y='crime_type',
        orientation='h',
        color='pct_21_23',
        text='pct_21_23'
    )

    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(filtered_trends, use_container_width=True)

# =========================
# TAB 5: WOMEN CRIME
# =========================
with tab5:
    st.subheader("👩 Women Crime Analysis")

    if not df_women.empty:

        threshold = st.slider("Min Women Crime %", 0.0, 50.0, 5.0)

        filtered_women = df_women[df_women['women_crime_percentage'] >= threshold]

        top = filtered_women.sort_values(by='women_crime_percentage', ascending=False).iloc[0]

        st.warning(f"Highest Women Crime %: {top['state']} ({top['women_crime_percentage']:.2f}%)")

        fig = px.bar(
            filtered_women.sort_values(by='women_crime_percentage'),
            x='women_crime_percentage',
            y='state',
            orientation='h',
            color='women_crime_percentage',
            text='women_crime_percentage'
        )

        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(filtered_women, use_container_width=True)

    else:
        st.error("No data available")

# =========================
# TAB 6: MAP
# =========================
with tab6:
    st.subheader("🗺️ India Crime Map (2023)")

    with open("india_states.geojson") as f:
        geojson = json.load(f)

    map_data = df_total[df_total['year'] == 2023].copy()

    map_data['state'] = map_data['state'].str.strip().str.lower()

    for feature in geojson["features"]:
        feature["properties"]["NAME_1"] = feature["properties"]["NAME_1"].strip().lower()

    state_mapping = {
        "andaman & nicobar islands": "andaman and nicobar",
        "delhi": "nct of delhi",
        "odisha": "orissa"
    }

    map_data['state'] = map_data['state'].replace(state_mapping)

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

    st.subheader("📋 Data Table")
    st.dataframe(map_data.sort_values(by='total_crimes', ascending=False), use_container_width=True)