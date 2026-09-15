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

Click on any preview image below to interact with the live dashboard on Tableau Public:

| Visualization | Live Preview |
| :--- | :--- |
| **Spatial Symbol Map**<br> *Geographic tracking across 30 stations* | [![Symbol Map Preview](./docs/map.png)](https://public.tableau.com/views/Book2_17894889785510/map) |
| **6-Month AQI Forecast**<br> *Predictive time-series modeling* | [![Forecast Preview](./docs/forecast.png)](https://public.tableau.com/views/Book3_17894907559570/Sheet1) |
| **Seasonal AQI Analysis**<br> *Winter spikes vs. Monsoon recovery* | [![Seasonal Preview](./docs/seasonal.png)](https://public.tableau.com/views/Book4_17894911840480/Sheet1) |
| **Monthly Trend Line**<br> *Time-series pollution shifts* | [![Trend Preview](./docs/trend.png)](https://public.tableau.com/views/Book5_17894915469430/Sheet1) |

---
For additional details and individual sheet breakdowns, see our [Dashboard Links Documentation](./dashboard_link.md).
