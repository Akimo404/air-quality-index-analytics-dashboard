"""
Delhi AQI 2023 Data Preprocessing Pipeline
Exact replication of the Colab notebook workflow for Tableau dashboard.
"""

from pathlib import Path
import pandas as pd
import numpy as np

# 1. CONFIGURATION
CONFIG = {
    'MONTH_MAP': {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
}

# 2. STATION COORDINATES (Matching exact Tableau dashboard coordinates)
STATION_COORDS = {
    'Alipur': (28.8170, 77.1190),
    'Anand Vihar': (28.6468, 77.3160),
    'Ashok Vihar': (28.6954, 77.1817),
    'Aya Nagar': (28.4565, 77.1155),
    'Burari Crossing': (28.7465, 77.2120),
    'CRRI Mathura Road': (28.5400, 77.2900),
    'Chandni Chowk Delhi IITM': (28.6538, 77.2300),
    'DTU': (28.7500, 77.1170),
    'Dwarka': (28.5766, 77.0766),
    'ITO': (28.6286, 77.2411),
    'Jahangirpuri': (28.7328, 77.1706),
    'Jawaharlal Nehru Stadium': (28.5803, 77.2338),
    'Lodhi Road Delhi IITM': (28.5908, 77.2264),
    'Major Dhyan Chand National Stadium': (28.6114, 77.2377),
    'Mandir Marg': (28.6364, 77.2011),
    'Mundka': (28.6824, 77.0306),
    'Najafgarh': (28.6092, 76.9798),
    'Narela': (28.8228, 77.1020),
    'Nehru Nagar': (28.5672, 77.2502),
    'North Campus': (28.6890, 77.2050),
    'Okhla': (28.5308, 77.2713),
    'Patparganj': (28.6237, 77.2872),
    'Punjabi Bagh': (28.6742, 77.1313),
    'Pusa': (28.6370, 77.1770),
    'RK Puram': (28.5644, 77.1903),
    'Rohini': (28.7325, 77.1199),
    'Shadipur': (28.6478, 77.1476),
    'Siri Fort': (28.5500, 77.2167),
    'Sonia Vihar': (28.7105, 77.2495),
    'Wazirpur': (28.6998, 77.1655)
}

# 3. 2023 DELHI FESTIVALS & HOLIDAYS
HOLIDAY_DICT = {
    '2023-01-01': 'New Year',
    '2023-01-14': 'Lohri',
    '2023-01-26': 'Republic Day',
    '2023-03-07': 'Holika Dahan',
    '2023-03-08': 'Holi',
    '2023-10-24': 'Dussehra',
    '2023-11-12': 'Diwali',
    '2023-11-13': 'Diwali Day 2',
    '2023-11-14': 'Bhai Dooj',
    '2023-12-25': 'Christmas'
}


def get_project_root() -> Path:
    """Returns the root directory of the repository."""
    return Path(__file__).resolve().parent.parent


def extract_station_name(filepath: Path) -> str:
    """Extracts and standardizes monitoring station names from file stems."""
    stem = filepath.stem
    stem = stem.replace('AQI_daily_2023_', '').replace('DelhiDPCC_2023_', '')
    stem = stem.replace('DelhiDPCC', '').replace('_2023', '')
    stem = stem.replace('_', ' ')
    stem = stem.replace(' (1)', '').replace(' (2)', '')
    stem = stem.replace('Delhi DPCC', '').replace('Delhi IMD', '').replace('Delhi CPCB', '')
    stem = stem.replace('Phase-2', '').replace('Sector 8', '')
    stem = stem.replace('R K Puram', 'RK Puram')
    stem = stem.replace('Sirifort', 'Siri Fort')
    stem = stem.replace('North Campus DU', 'North Campus')
    stem = stem.replace('Dwarka-', 'Dwarka')
    return stem.strip()


def load_one_file(filepath: Path) -> pd.DataFrame:
    """Loads one Excel file, extracts station metadata, and melts matrix format into long format."""
    station = extract_station_name(filepath)
    df = pd.read_excel(filepath, header=0, nrows=31, engine='openpyxl')

    df_long = df.melt(id_vars=['Day'], var_name='Month', value_name='AQI')
    df_long['MonthNum'] = df_long['Month'].map(CONFIG['MONTH_MAP'])

    df_long['Date'] = pd.to_datetime(
        '2023-' + df_long['MonthNum'].astype(str) + '-' + df_long['Day'].astype(str),
        format='%Y-%m-%d',
        errors='coerce'
    )
    df_long = df_long.dropna(subset=['Date'])

    df_long['AQI'] = pd.to_numeric(df_long['AQI'], errors='coerce')
    df_long['Station'] = station

    coords = STATION_COORDS.get(station, (np.nan, np.nan))
    df_long['Latitude'] = coords[0]
    df_long['Longitude'] = coords[1]

    return df_long[['Date', 'Station', 'Latitude', 'Longitude', 'AQI']].sort_values('Date').reset_index(drop=True)


def load_raw_data(raw_dir: Path) -> pd.DataFrame:
    """Batch loads all raw Excel files from the target directory."""
    files = list(raw_dir.glob('*.xlsx')) + list(raw_dir.glob('*.xls'))
    if not files:
        raise FileNotFoundError(f"No Excel files found in {raw_dir}")

    print(f"📁 Found {len(files)} Excel files in {raw_dir}")
    dfs = []
    for f in files:
        df_one = load_one_file(f)
        print(f"  - {extract_station_name(f)}: {len(df_one)} rows")
        dfs.append(df_one)

    df_combined = pd.concat(dfs, ignore_index=True)
    return df_combined.sort_values(['Station', 'Date']).reset_index(drop=True)


def impute_group(s: pd.Series) -> pd.Series:
    """Applies forward fill followed by linear interpolation per station."""
    s = s.ffill()
    s = s.interpolate(method='linear', limit_direction='both')
    return s.round(0)


def get_season(month: int) -> str:
    """Categorizes months into Delhi seasons."""
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Summer'
    else:
        return 'Post-Monsoon'


def clean_aqi_data(df: pd.DataFrame) -> pd.DataFrame:
    """Executes missing value imputation, outlier detection, feature engineering, and risk binnings."""

    # 1. Missing Value Imputation
    print("🧹 Imputing missing AQI values...")
    df['AQI'] = df.groupby('Station')['AQI'].transform(impute_group).astype(int)

    # 2. Outlier Flags (IQR and Z-Score per station)
    print("🔍 Flagging outliers...")
    iqr_lb = df.groupby('Station')['AQI'].transform(
        lambda s: round(s.quantile(0.25) - 1.5 * (s.quantile(0.75) - s.quantile(0.25)), 1)
    )
    iqr_ub = df.groupby('Station')['AQI'].transform(
        lambda s: round(s.quantile(0.75) + 1.5 * (s.quantile(0.75) - s.quantile(0.25)), 1)
    )
    outlier_iqr = (df['AQI'] < iqr_lb) | (df['AQI'] > iqr_ub)

    zscore = df.groupby('Station')['AQI'].transform(
        lambda s: round((s - s.mean()) / s.std(), 2)
    )
    outlier_zscore = np.abs(zscore) > 3

    df['Outlier_IQR'] = outlier_iqr.astype(int)
    df['Outlier_Zscore'] = outlier_zscore.astype(int)
    df['Outlier_Either'] = (outlier_iqr | outlier_zscore).astype(int)
    df['Outlier_Both'] = (outlier_iqr & outlier_zscore).astype(int)
    df['ZScore'] = zscore
    df['IQR_LowerBound'] = iqr_lb
    df['IQR_UpperBound'] = iqr_ub

    # 3. Feature Engineering & Date Transformations
    print("⚙️ Building time features and holiday tags...")
    holiday_map = pd.Series(list(HOLIDAY_DICT.values()), index=pd.to_datetime(list(HOLIDAY_DICT.keys())))
    df['IsHoliday'] = df['Date'].isin(holiday_map.index).astype(int)
    df['HolidayName'] = df['Date'].map(holiday_map).fillna('Regular Day')

    df['Season'] = df['Date'].dt.month.apply(get_season)
    df['SeasonOrdinal'] = df['Season'].map({'Winter': 1, 'Summer': 2, 'Monsoon': 3, 'Post-Monsoon': 4})

    df['MonthName'] = df['Date'].dt.month_name()
    df['MonthNum'] = df['Date'].dt.month
    df['Quarter'] = df['Date'].dt.quarter
    df['DayofWeek'] = df['Date'].dt.day_name()
    df['WeekNum'] = df['Date'].dt.isocalendar().week.astype(int)
    df['IsWeekend'] = df['Date'].dt.dayofweek.isin([5, 6]).astype(int)
    df['IsWinter'] = df['Date'].dt.month.isin([11, 12, 1, 2]).astype(int)

    # 4. Asthma Risk Classification for Choropleth & Risk Charts
    df['Asthma_Risk'] = pd.cut(
        df['AQI'],
        bins=[0, 50, 100, float('inf')],
        labels=['Safe', 'Caution', 'Unsafe']
    )

    # Reorder columns to match exact target schema
    target_columns = [
        'Date', 'Station', 'Latitude', 'Longitude', 'AQI', 'Outlier_IQR',
        'Outlier_Zscore', 'Outlier_Either', 'Outlier_Both', 'ZScore',
        'IQR_LowerBound', 'IQR_UpperBound', 'IsHoliday', 'HolidayName',
        'Season', 'SeasonOrdinal', 'MonthName', 'MonthNum', 'Quarter',
        'DayofWeek', 'WeekNum', 'IsWeekend', 'IsWinter', 'Asthma_Risk'
    ]
    return df[target_columns]


def main():
    root_dir = get_project_root()
    raw_dir = root_dir / "data" / "raw"
    processed_dir = root_dir / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    print("--- Starting AQI Data Preprocessing ---")

    raw_df = load_raw_data(raw_dir)
    cleaned_df = clean_aqi_data(raw_df)

    output_path = processed_dir / "delhi_aqi_2023_tableau_ready.csv"
    cleaned_df.to_csv(output_path, index=False, date_format='%Y-%m-%d')

    print(f"\n💾 Saved processed dataset to: {output_path}")
    print("✅ Ready for Tableau Dashboard!")


if __name__ == "__main__":
    main()
