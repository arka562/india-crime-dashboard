import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Page config (MUST BE FIRST)
st.set_page_config(
    page_title="India Crime Dashboard",
    page_icon="🚔",
    layout="wide"
)

st.title("India Crime Dashboard")

st.markdown("""
### 📊 Overview
This dashboard analyzes crime trends across India using NCRB data.
Use filters from the sidebar to explore insights.
""")

# Load data
df = pd.read_csv("ncrb_crime_types_all_years.csv")
df_pct = pd.read_csv("ncrb_crime_pct_changes.csv")

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("📊 Dashboard Filters")

states = df['state'].unique()
selected_states = st.sidebar.multiselect(
    "Select States",
    options=states,
    default=states[:3]
)

crime_types = df['crime_type'].unique()
selected_crime = st.sidebar.selectbox(
    "Select Crime Type",
    options=crime_types
)

# =========================
# FILTER DATA
# =========================
filtered_df = df[
    (df['state'].isin(selected_states)) &
    (df['crime_type'] == selected_crime)
]

# =========================
# DOWNLOAD BUTTON
# =========================
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name='filtered_crime_data.csv',
    mime='text/csv',
)

# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Trends",
    "🗺️ State View",
    "📊 % Change Analysis",
    "🌍 India Map"
])

# =========================
# TAB 1: TRENDS
# =========================
with tab1:

    st.write("## Key Insights")

    latest_data = filtered_df[filtered_df['year'] == 2023]
    prev_data = filtered_df[filtered_df['year'] == 2021]

    total_2023 = latest_data['count'].sum()
    total_2021 = prev_data['count'].sum()

    pct_change = ((total_2023 - total_2021) / total_2021) * 100 if total_2021 != 0 else 0

    col1, col2 = st.columns(2)
    col1.metric("Total Cases (2023)", f"{int(total_2023):,}")
    col2.metric("Growth %", f"{pct_change:.2f}%")

    st.write("### Crime Trend Comparison")

    fig = px.line(
        filtered_df,
        x='year',
        y='count',
        color='state',
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 2: STATE VIEW
# =========================
with tab2:

    st.write("## State Ranking (2023)")

    data_2023 = filtered_df[filtered_df['year'] == 2023]

    fig2 = px.bar(
        data_2023,
        x='count',
        y='state',
        orientation='h',
        color='count'
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Top & Bottom states
    top_states = data_2023.sort_values(by='count', ascending=False).head(5)
    bottom_states = data_2023.sort_values(by='count', ascending=True).head(5)

    col1, col2 = st.columns(2)

    with col1:
        st.write("### 🔴 Top 5 States (Highest Crime)")
        st.dataframe(top_states[['state', 'count']])

    with col2:
        st.write("### 🟢 Safest 5 States")
        st.dataframe(bottom_states[['state', 'count']])

# =========================
# TAB 3: % CHANGE
# =========================
with tab3:

    st.write("## % Change Analysis (2021 → 2023)")

    crime_data = df_pct[df_pct['crime_type'] == selected_crime]
    crime_data = crime_data.sort_values(by='pct_21_23', ascending=True)

    fig = px.bar(
        crime_data,
        x='pct_21_23',
        y='crime_type',
        orientation='h',
        title='Crime % Change (2021–2023)',
        labels={'pct_21_23': '% Change'},
        color='pct_21_23'
    )

    st.plotly_chart(fig, use_container_width=True)

    if not crime_data.empty:
        max_row = crime_data.loc[crime_data['pct_21_23'].idxmax()]
        min_row = crime_data.loc[crime_data['pct_21_23'].idxmin()]

        st.success(f"Highest Increase: {max_row['pct_21_23']:.2f}%")
        st.info(f"Lowest / Decrease: {min_row['pct_21_23']:.2f}%")

# =========================
# TAB 4: MAP
# =========================
with tab4:

    st.write("## India Crime Map (2023)")

    with open("india_states.geojson") as f:
        geojson = json.load(f)

    map_data = filtered_df[filtered_df['year'] == 2023]
    map_data = map_data.groupby('state')['count'].sum().reset_index()

    # Normalize
    map_data['state'] = map_data['state'].str.strip().str.lower()

    for feature in geojson["features"]:
        feature["properties"]["NAME_1"] = feature["properties"]["NAME_1"].strip().lower()

    # Fix mismatches
    state_map = {
        "andaman and nicobar islands": "andaman and nicobar",
        "odisha": "orissa"
    }

    map_data['state'] = map_data['state'].replace(state_map)

    fig = px.choropleth(
        map_data,
        geojson=geojson,
        featureidkey="properties.NAME_1",
        locations="state",
        color="count",
        color_continuous_scale="Reds",
        title="Crime Distribution Across India"
    )

    fig.update_geos(fitbounds="locations", visible=False)

    st.plotly_chart(fig, use_container_width=True)

    st.caption("Darker regions indicate higher crime levels in 2023")