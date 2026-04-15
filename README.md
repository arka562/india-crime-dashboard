# 🚔 India Crime Dashboard

An interactive data analytics dashboard to explore crime trends across India using NCRB datasets.

🔗 Live App:
https://india-crime-dashboard-s3nmqhlxqnxjze74yj2vdn.streamlit.app/

---

## 📊 Overview

This project transforms complex crime data into an interactive dashboard that allows users to explore patterns, trends, and insights across different states and crime categories in India.

The goal is to make large-scale public data understandable, visual, and actionable.

---

## 🚀 Features

### 🔍 Interactive Filters

* Select multiple states
* Choose specific crime types
* Dynamic updates across all visualizations

### 📈 Trend Analysis

* Year-wise crime trends
* Growth comparison between 2021 and 2023
* Multi-state comparison

### 🗺️ State-Level Insights

* State-wise crime ranking
* Top 5 highest crime states
* Safest states

### 📊 Percentage Change Analysis

* Crime increase/decrease insights

### 🌍 Geospatial Visualization

* Interactive India choropleth map
* Color-coded crime intensity

### 📥 Data Export

* Download filtered dataset as CSV

---

## 🛠️ Tech Stack

* Streamlit
* Pandas
* Plotly
* GeoJSON

---

## 📂 Project Structure

india-crime-dashboard/
│
├── app.py
├── ncrb_crime_types_all_years.csv
├── ncrb_crime_pct_changes.csv
├── india_states.geojson
├── requirements.txt
└── README.md

---

## ⚙️ How to Run Locally

1. Clone the repository
   git clone https://github.com/YOUR-USERNAME/india-crime-dashboard.git

2. Navigate to folder
   cd india-crime-dashboard

3. Install dependencies
   pip install -r requirements.txt

4. Run the app
   streamlit run app.py

---

## 📌 Key Insights

* Crime varies significantly across states
* Some states consistently report higher crime rates
* Certain crime categories show growth trends
* Map visualization reveals regional patterns

---

## 🧠 Challenges Faced

* State name mismatch between dataset and GeoJSON
* Deployment debugging on Streamlit Cloud
* Designing multi-tab interactive dashboard

---

## 💡 Learnings

* Built end-to-end data dashboard
* Improved data visualization & storytelling
* Learned cloud deployment
* Handled real-world messy datasets

---

## 💼 Resume Description

Developed and deployed an interactive India Crime Analytics Dashboard using Streamlit, Pandas, and Plotly, featuring multi-filter analysis, trend visualization, and geospatial mapping to uncover crime patterns across states.

---

## 📸 Screenshots

(Add screenshots here)

Example:
![Dashboard](images/dashboard.png)
![Map](images/map.png)

---

## 🔥 Future Improvements

* Add ML-based crime prediction
* District-level analysis
* UI improvements

---

## 👨‍💻 Author

Arkaprava Ghosh

---

## ⭐ Support

If you liked this project, give it a star ⭐
