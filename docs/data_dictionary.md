# 📖 Data Dictionary

This document details the attributes, data types, logic, and descriptions for all 24 columns in the processed dataset (`data/processed/delhi_aqi_2023_tableau_ready.csv`).

---

## Column Specifications

| Column Name | Data Type | Sample Value | Description & Business Logic |
| :--- | :--- | :--- | :--- |
| **`Date`** | `Date` | `2023-01-01` | Date of reading formatted as `YYYY-MM-DD`. Spans all 365 days of 2023. |
| **`Station`** | `String` | `Anand Vihar` | Standardized monitoring station name (30 total stations across Delhi). |
| **`Latitude`** | `Float` | `28.6468` | Precise WGS84 latitude for mapping and spatial analysis in Tableau. |
| **`Longitude`** | `Float` | `27.3160` | Precise WGS84 longitude for mapping and spatial analysis in Tableau. |
| **`AQI`** | `Integer` | `330` | Daily Air Quality Index value. Missing raw values imputed via station-grouped forward fill and linear interpolation. |
| **`Outlier_IQR`** | `Binary (0/1)` | `0` | Flagged as `1` if $\text{AQI} < Q_1 - 1.5 \times \text{IQR}$ or $\text{AQI} > Q_3 + 1.5 \times \text{IQR}$ per station. |
| **`Outlier_Zscore`** | `Binary (0/1)` | `0` | Flagged as `1` if the station-relative Z-score exceeds $\vert{}Z\vert{} > 3$. |
| **`Outlier_Either`** | `Binary (0/1)` | `0` | Flagged as `1` if detected as an outlier by either IQR or Z-Score logic. |
| **`Outlier_Both`** | `Binary (0/1)` | `0` | Flagged as `1` if detected as an outlier by both IQR and Z-Score logic simultaneously. |
| **`ZScore`** | `Float` | `1.45` | Number of standard deviations from the station's annual mean AQI: $\frac{x - \mu}{\sigma}$. |
| **`IQR_LowerBound`** | `Float` | `112.5` | Lower dynamic cutoff bound calculated per station for anomaly detection. |
| **`IQR_UpperBound`** | `Float` | `487.5` | Upper dynamic cutoff bound calculated per station for anomaly detection. |
| **`IsHoliday`** | `Binary (0/1)` | `1` | Flagged as `1` on major Delhi festival/holiday dates (e.g., Diwali, Holi). |
| **`HolidayName`** | `String` | `Diwali` | Name of the holiday/festival (defaults to `Regular Day`). |
| **`Season`** | `String` | `Winter` | Categorical Delhi season tag (*Winter*, *Summer*, *Monsoon*, *Post-Monsoon*). |
| **`SeasonOrdinal`** | `Integer` | `1` | Ordinal encoding for season filtering (1 = Winter, 2 = Summer, 3 = Monsoon, 4 = Post-Monsoon). |
| **`MonthName`** | `String` | `January` | Full name of the calendar month. |
| **`MonthNum`** | `Integer` | `1` | Numerical month representation (1–12). |
| **`Quarter`** | `Integer` | `1` | Calendar quarter (Q1–Q4). |
| **`DayofWeek`** | `String` | `Sunday` | Full day name of the reading date. |
| **`WeekNum`** | `Integer` | `52` | ISO calendar week number (1–52). |
| **`IsWeekend`** | `Binary (0/1)` | `1` | Flagged as `1` if the day falls on Saturday or Sunday. |
| **`IsWinter`** | `Binary (0/1)` | `1` | Flagged as `1` for severe pollution months (November, December, January, February). |
| **`Asthma_Risk`** | `Categorical` | `Unsafe` | Health risk classification based on AQI value thresholds (*Safe*: $\le 50$, *Caution*: $51\text{--}100$, *Unsafe*: $> 100$). |
