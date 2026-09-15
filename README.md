# 🫁 Delhi Air Quality Index (AQI) Analytics & Tableau Dashboard

An end-to-end data engineering and analytics pipeline designed to ingest, clean, feature-engineer, and analyze daily Air Quality Index (AQI) data across **30 monitoring stations in Delhi** for 2023 (10,950 total readings). 

This repository transforms raw, matrix-formatted Excel files into a standardized, spatial, and feature-rich dataset optimized for **Tableau visualizations** and health risk modeling.

---

## 📁 Repository Structure

```text
air-quality-index-analytics-dashboard/
│
├── dashboard/                  # Tableau dashboard links and documentation
│   └── tableau_dashboard_link.md
│
├── data/
│   ├── raw/                    # 30 Raw CPCB/DPCC/IMD Excel files (.xlsx)
│   └── processed/              # Cleaned, Tableau-ready dataset (.csv)
│       └── delhi_aqi_2023_tableau_ready.csv
│
├── docs/                       # Project methodology and technical write-ups
│   └── methodology.md
│
├── notebooks/                  # Exploratory Data Analysis & Colab notebooks
│   └── Data_Preprocessing.ipynb and AQI calculator
│
├── src/
│   └── preprocess.py           # Production data preprocessing pipeline
│
├── .gitignore                  # Git ignore rules for data and environment files
├── README.md                   # Project overview & documentation
└── requirements.txt            # Python library dependencies

## 📊 Interactive Dashboards & Visualizations

Click on any preview image below to launch the live interactive dashboard on Tableau Public:

<table>
  <tr>
    <td align="center"><b>Spatial Symbol Map</b><br><i>30 monitoring stations</i></td>
    <td align="center">
      <a href="https://public.tableau.com/views/Book2_17894889785510/map">
        <img src="Symbol Map.png" width="400" alt="Symbol Map Preview">
      </a>
    </td>
  </tr>
  <tr>
    <td align="center"><b>6-Month AQI Forecast</b><br><i>Predictive time-series model</i></td>
    <td align="center">
      <a href="https://public.tableau.com/views/Book3_17894907559570/Sheet1">
        <img src="Forecast.png" width="400" alt="Forecast Preview">
      </a>
    </td>
  </tr>
  <tr>
    <td align="center"><b>Seasonal AQI Analysis</b><br><i>Winter spikes vs Monsoon recovery</i></td>
    <td align="center">
      <a href="https://public.tableau.com/views/Book4_17894911840480/Sheet1">
        <img src="Seasons.png" width="400" alt="Seasonal Preview">
      </a>
    </td>
  </tr>
  <tr>
    <td align="center"><b>Station Rankings & Trend</b><br><i>Comparative metrics</i></td>
    <td align="center">
      <a href="https://public.tableau.com/views/Book5_17894915469430/Sheet1">
        <img src="Rankings.png" width="400" alt="Rankings Preview">
      </a>
    </td>
  </tr>
</table>

---
For detailed breakdowns, see our <a href="./dashboard_link.md">Dashboard Links Documentation</a>.
