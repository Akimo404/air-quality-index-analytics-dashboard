# 🔬 Technical Methodology & Pipeline Architecture

This document outlines the data engineering workflow, transformation rules, statistical anomaly detection, and feature modeling applied to the 2023 Delhi Air Quality Index (AQI) dataset.

---

## 🏗️ 1. Pipeline Architecture

The ETL pipeline is structured into four sequential stages executed by `src/preprocess.py`:

```text
[ Raw Excel Files ] ──> [ Unpivoting & Cleaning ] ──> [ Imputation & Outliers ] ──> [ Feature Engineering ] ──> [ Tableau CSV ]
