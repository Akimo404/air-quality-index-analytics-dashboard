import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# 1. STATION COORDINATES (Delhi 2023 Monitoring Stations)
STATION_COORDS = {
    "Anand Vihar": (28.6468, 77.3160),
    "Ashok Vihar": (28.6954, 77.1817),
    "Bawana": (28.7762, 77.0511),
    "DTU": (28.7490, 77.1170),
    "Dwarka Sector 8": (28.5710, 77.0719),
    "IHBAS Dilshad Garden": (28.6811, 77.3150),
    "Ito": (28.6286, 77.2410),
    "Jahangirpuri": (28.7328, 77.1706),
    "Jawaharlal Nehru Stadium": (28.5802, 77.2338),
    "Major Dhyan Chand National Stadium": (28.6119, 77.2376),
    "Mandir Marg": (28.6360, 77.2010),
    "Mundka": (28.6847, 77.0762),
    "Najafgarh": (28.6090, 76.9798),
    "Narela": (28.8228, 77.0928),
    "Okhla Phase 2": (28.5308, 77.2712),
    "Patparganj": (28.6235, 77.2872),
    "Punjabi Bagh": (28.6683, 77.1167),
    "R K Puram": (28.5632, 77.1869),
    "Rohini": (28.7325, 77.1199),
    "Sonia Vihar": (28.7106, 77.2475),
    "Vivek Vihar": (28.6724, 77.3153)
}

# 2. 2023 DELHI HOLIDAYS & EVENTS
HOLIDAYS_2023 = {
    "2023-01-26": "Republic Day",
    "2023-03-08": "Holi",
    "2023-04-07": "Good Friday",
    "2023-04-22": "Eid-ul-Fitr",
    "2023-08-15": "Independence Day",
    "2023-09-07": "Janmashtami",
    "2023-09-09": "G20 Summit Delhi",
    "2023-09-10": "G20 Summit Delhi",
    "2023-10-02": "Gandhi Jayanti",
    "2023-10-24": "Dussehra",
    "2023-11-12": "Diwali",
    "2023-11-27": "Guru Nanak Jayanti",
    "2023-12-25": "Christmas Day"
}

def get_season(month: int) -> str:
    """Classifies month into Delhi seasonal periods."""
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5, 6]:
        return "Summer"
    elif month in [7, 8, 9]:
        return "Monsoon"
    else:
        return "Post-Monsoon"

def get_project_root() -> Path:
    """Returns the root directory of the repository."""
    return Path(__file__).resolve().parent.parent

def transform_cpcb_matrix(df_raw: pd.DataFrame, file_path: Path) -> pd.DataFrame:
    """Transforms raw CPCB matrix files (Day x Month) into tabular long format."""
    month_cols = [col for col in df_raw.columns if col != "Day"]
    df_long = df_raw.melt(id_vars=["Day"], value_vars=month_cols, var_name="Month_Name", value_name="AQI")
    
    station_name = file_path.stem.replace("_2023", "").replace("_", " ").strip()
    df_long["station"] = station_name
    df_long["date_str"] = "2023 " + df_long["Month_Name"].astype(str) + " " + df_long["Day"].astype(str)
    df_long["date"] = pd.to_datetime(df_long["date_str"], format="%Y %B %d", errors="coerce")
    
    return df_long.dropna(subset=["date"])[["date", "station", "AQI"]]

def load_raw_data(raw_dir: Path) -> pd.DataFrame:
    """Reads all raw CSV and Excel files from the raw data directory."""
    all_files = list(raw_dir.glob("*.csv")) + list(raw_dir.glob("*.xlsx")) + list(raw_dir.glob("*.xls"))

    if not all_files:
        raise FileNotFoundError(f"No raw CSV or Excel files found in {raw_dir}")

    df_list = []
    for file_path in all_files:
        print(f"Loading: {file_path.name}")
        if file_path.suffix == ".csv":
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
            
        # Handle matrix CPCB structure if "Day" exists in columns
        if "Day" in df.columns:
            df = transform_cpcb_matrix(df, file_path)
            
        df_list.append(df)

    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df

def clean_aqi_data(df: pd.DataFrame) -> pd.DataFrame:
    """Executes cleaning, imputation, feature engineering, and metadata mapping on AQI data."""
    # 1. Standardize column names
    df.columns = (
        df.columns.str.strip().str.lower().str.replace(" ", "_")
    )

    # 2. Convert and format dates
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
        df["month_name"] = df["date"].dt.strftime("%B")
        df["month"] = df["date"].dt.month
        df["year"] = df["date"].dt.year
        df["quarter"] = "Q" + df["date"].dt.quarter.astype(str)
        df["week_number"] = df["date"].dt.isocalendar().week
        df["day_of_week"] = df["date"].dt.day_name()
        df["is_weekend"] = df["date"].dt.dayofweek >= 5

    # 3. Standardize station names if present
    if "station" in df.columns:
        df["station"] = df["station"].astype(str).str.strip().str.title()
        df["latitude"] = df["station"].map(lambda x: STATION_COORDS.get(x, (np.nan, np.nan))[0])
        df["longitude"] = df["station"].map(lambda x: STATION_COORDS.get(x, (np.nan, np.nan))[1])

    # 4. Handle missing AQI values (linear interpolation + forward fill per station)
    if "aqi" in df.columns:
        df["aqi"] = pd.to_numeric(df["aqi"], errors="coerce")
        if "station" in df.columns:
            df["aqi"] = (
                df.groupby("station")["aqi"]
                .transform(lambda group: group.interpolate(method="linear").ffill().bfill())
            )
        else:
            df["aqi"] = df["aqi"].interpolate(method="linear").ffill().bfill()

        # 5. Categorize AQI Risk Levels
        bins = [-np.inf, 100, 200, np.inf]
        labels = ["Safe", "Caution", "Unsafe"]
        df["asthma_risk"] = pd.cut(df["aqi"], bins=bins, labels=labels)

    # 6. Event and Season Categorization
    date_str_series = df["date"].dt.strftime("%Y-%m-%d")
    df["holiday_name"] = date_str_series.map(HOLIDAYS_2023).fillna("None")
    df["is_holiday"] = df["holiday_name"] != "None"
    df["season"] = df["month"].apply(get_season)

    return df

def main():
    root_dir = get_project_root()
    raw_dir = root_dir / "data" / "raw"
    processed_dir = root_dir / "data" / "processed"

    # Ensure processed folder exists
    processed_dir.mkdir(parents=True, exist_ok=True)

    print("--- Starting AQI Data Preprocessing ---")

    # Load
    raw_df = load_raw_data(raw_dir)

    # Clean
    cleaned_df = clean_aqi_data(raw_df)

    # Export
    output_path = processed_dir / "delhi_aqi_processed.csv"
    cleaned_df.to_csv(output_path, index=False)

    print(f"--- Processing Complete! Processed file saved to: {output_path} ---")

if __name__ == "__main__":
    main()
