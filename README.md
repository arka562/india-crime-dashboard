# 🚔 India Crime Analytics Dashboard

## 📊 Overview

An interactive data analytics dashboard built using **Streamlit** to analyze crime trends across India based on NCRB datasets.

The project processes multi-year crime data and provides insights into:

* State-wise crime distribution
* Year-over-year growth trends
* Crime category analysis
* Crimes against women
* Geospatial crime mapping

---

## 🚀 Features

### 🔍 Interactive Filters

* Select states and crime types
* Search functionality
* Dynamic filtering across all views

### 📈 Analytics

* Crime trends (2021–2023)
* State ranking (Top/Bottom analysis)
* Year-over-Year growth
* Crime-type growth insights

### 👩 Women Safety Analysis

* Crimes against women by state
* Percentage-based comparison
* High-risk state identification

### 🗺️ Geo Visualization

* Choropleth map of India
* State-wise crime intensity

### 📊 Data Engineering

* Cleaned and transformed raw NCRB datasets
* Built reusable ETL pipelines
* Generated multiple analytical datasets

---

## 🛠️ Tech Stack

* **Python**
* **Pandas**
* **Streamlit**
* **Plotly**
* **GeoJSON**

---

## 📂 Project Structure

```
project/
│
├── data/
│   ├── ncrb_master_dataset.csv
│   ├── ncrb_total_trends.csv
│   ├── ncrb_yoy_changes.csv
│   ├── ncrb_crime_trends.csv
│   ├── ncrb_women_analysis_2023.csv
│
├── app.py
├── india_states.geojson
└── README.md
```

---

## ⚙️ How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📌 Key Insights

* Identified states with highest crime growth
* Highlighted trends in crimes against women
* Built a complete crime analysis pipeline from raw data

---

## 🌟 Future Improvements

* ML-based crime prediction
* AI-generated insights
* Real-time data integration

---

## 👨‍💻 Author

Arkaprava Ghosh
