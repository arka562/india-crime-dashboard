import streamlit as st
import pandas as pd
import plotly.express as px
import json
from crime_model import predict_crime

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="India Crime Dashboard", layout="wide")

# =========================
# 🎨 UI
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
    df_pop = pd.read_csv("state_population.csv")

    # Clean columns
    for df in [df_master, df_total, df_yoy, df_trends, df_women, df_pop]:
        df.columns = df.columns.str.strip().str.lower()

    return df_master, df_total, df_yoy, df_trends, df_women, df_pop

df_master, df_total, df_yoy, df_trends, df_women, df_pop = load_data()

# =========================
# SIDEBAR
# =========================
st.sidebar.header("📊 Filters")

states = sorted(df_master['state'].unique())
crime_types = sorted(df_master['crime_type'].unique())

selected_states = st.sidebar.multiselect("States", states, default=states[:5])
selected_crime = st.sidebar.selectbox("Crime Type", crime_types)

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
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📈 Trends",
    "🏆 State Ranking",
    "📊 YOY Growth",
    "📊 Crime Type Trends",
    "👩 Women Crime",
    "🗺️ Map",
    "🔮 Prediction",
    "📊 Per Capita"
])

# =========================
# TAB 1: Trends
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

# =========================
# TAB 2: Ranking
# =========================
with tab2:
    st.subheader("🏆 State Ranking (2023)")

    df_2023 = df_total[df_total['year'] == 2023]

    fig = px.bar(df_2023, x='total_crimes', y='state', orientation='h')
    st.plotly_chart(fig)

# =========================
# TAB 3: YOY
# =========================
with tab3:
    st.subheader("📊 Growth Analysis")

    fig = px.bar(df_yoy, x='pct_21_23', y='state', orientation='h')
    st.plotly_chart(fig)

# =========================
# TAB 4: Crime Type
# =========================
with tab4:
    st.subheader("📊 Crime Type Trends")

    fig = px.bar(df_trends, x='pct_21_23', y='crime_type', orientation='h')
    st.plotly_chart(fig)

# =========================
# TAB 5: Women
# =========================
with tab5:
    st.subheader("👩 Women Crime Analysis")

    fig = px.bar(df_women, x='women_crime_percentage', y='state', orientation='h')
    st.plotly_chart(fig)

# =========================
# TAB 6: Map
# =========================
with tab6:
    st.subheader("🗺️ India Crime Map")

    with open("india_states.geojson") as f:
        geojson = json.load(f)

    df_map = df_total[df_total['year'] == 2023].copy()
    df_map['state'] = df_map['state'].str.lower()

    fig = px.choropleth(
        df_map,
        geojson=geojson,
        locations="state",
        featureidkey="properties.NAME_1",
        color="total_crimes"
    )

    st.plotly_chart(fig)

# =========================
# TAB 7: ML
# =========================
with tab7:
    st.subheader("🔮 Prediction")

    df_actual = df_master.groupby(['state','year'])['count'].sum().reset_index()
    df_actual.rename(columns={'count':'crime'}, inplace=True)
    df_actual['type'] = 'Actual'

    df_pred = predict_crime(df_master)
    df_pred.rename(columns={'predicted_crime':'crime'}, inplace=True)
    df_pred['type'] = 'Predicted'

    df_all = pd.concat([df_actual, df_pred])

    state = st.selectbox("Select State", df_all['state'].unique())
    df_plot = df_all[df_all['state']==state]

    fig = px.line(df_plot, x='year', y='crime', color='type', markers=True)
    st.plotly_chart(fig)

# =========================
# TAB 8: PER CAPITA
# =========================
with tab8:
    st.subheader("📊 Crime per 100K Population")

    # Fix state column
    if 'state/ut' in df_pop.columns:
        df_pop.rename(columns={'state/ut': 'state'}, inplace=True)
    elif 'state' not in df_pop.columns:
        df_pop.rename(columns={df_pop.columns[0]: 'state'}, inplace=True)

    # Fix population column
    for col in df_pop.columns:
        if 'pop' in col:
            df_pop.rename(columns={col: 'population'}, inplace=True)

    # Clean values
    df_total['state'] = df_total['state'].str.strip().str.lower()
    df_pop['state'] = df_pop['state'].str.strip().str.lower()

    # Merge
    df_cap = df_total[df_total['year'] == 2023].merge(df_pop, on='state')

    # Compute
    df_cap['crime_per_100k'] = (
        df_cap['total_crimes'] / df_cap['population']
    ) * 100000

    fig = px.bar(
        df_cap.sort_values(by='crime_per_100k'),
        x='crime_per_100k',
        y='state',
        orientation='h'
    )

    st.plotly_chart(fig)
    st.dataframe(df_cap)