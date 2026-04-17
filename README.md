# 🚔 India Crime Analytics Dashboard

An end-to-end data analytics and visualization project built using **Python, Pandas, and Streamlit** to analyze crime trends in India using NCRB datasets (2021–2023).

---

## 📌 Project Overview

This project focuses on transforming raw government crime data into meaningful insights through:

* 📊 Data Cleaning & Transformation
* 📈 Trend Analysis
* 🔍 Interactive Visualizations
* 🔮 Crime Prediction (ML-based)
* ⚖️ Normalized Metrics (Per Capita Analysis)

The goal is to help understand **crime patterns, growth trends, and safety indicators across states in India**.

---

## 🚀 Features

### 📈 1. Crime Trends

* Year-wise crime analysis (2021–2023)
* Growth percentage calculation
* State-wise comparison

### 🏆 2. State Ranking

* Top & bottom states by total crimes
* Comparative visualization

### 📊 3. Year-over-Year Growth

* Percentage increase/decrease in crime
* Identification of high-growth states

### 📊 4. Crime Type Analysis

* Most common crime categories
* Trend comparison across years

### 👩 5. Crimes Against Women

* State-wise analysis
* Women crime percentage
* Safety comparison

### 🗺️ 6. India Crime Map

* Choropleth visualization
* State-level crime distribution

### 🔮 7. Crime Prediction (ML)

* Forecasts for 2024 & 2025
* Based on historical growth trends
* Actual vs Predicted comparison

### ⚖️ 8. Per Capita Analysis

* Crime per 100,000 population
* Fair comparison across states

---

## 🧠 Tech Stack

* **Frontend:** Streamlit
* **Backend/Data Processing:** Python, Pandas
* **Visualization:** Plotly
* **Machine Learning:** Trend-based forecasting (custom logic)
* **Data Source:** NCRB (Government of India)

---

## 📂 Project Structure

```
project/
│
├── app.py                       # Main Streamlit app
├── crime_model.py               # Prediction logic
│
├── data/
│   ├── ncrb_master_dataset.csv
│   ├── ncrb_total_trends.csv
│   ├── ncrb_yoy_changes.csv
│   ├── ncrb_crime_trends.csv
│   ├── ncrb_women_analysis_2023.csv
│   ├── state_population.csv
│
├── india_states.geojson
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/india-crime-dashboard.git
cd india-crime-dashboard
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Application

```bash
streamlit run app.py
```

---

## 📊 Key Insights

* Certain states show consistent growth in crime rates over time
* Crimes against women vary significantly across regions
* Per capita analysis reveals different patterns than absolute numbers
* Some crime categories are increasing faster than others

---

## 🧠 Machine Learning Approach

* Used **trend-based forecasting** due to limited data (3 years)
* Calculated average growth rate per state
* Predicted future crime values (2024, 2025)
* Ensured robustness by handling edge cases like zero values

---

## 🎯 Challenges Faced

* Cleaning messy Excel datasets with inconsistent formatting
* Handling missing and malformed data
* Standardizing state names across multiple datasets
* Avoiding division-by-zero errors in growth calculations
* Ensuring correct dataset merging

---

## 🚀 Future Improvements

* Add advanced ML models (ARIMA, LSTM)
* Integrate real-time data APIs
* Include population trends over time
* Add alert system for high-risk states
* Deploy with cloud scaling

---

## 👨‍💻 Author

**Arkaprava Ghosh**

* Aspiring Software Developer & Data Analyst
* Focused on building real-world, impactful projects

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and feel free to contribute!
