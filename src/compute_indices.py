"""
ClimaZoneAI — Compute Renewable Energy Indices
----------------------------------------------
1. Loads cleaned_data.csv from preprocessing step.
2. Computes Solar, Wind, and Hydro indices.
3. Normalizes each index to [0,1].
4. Calculates Renewable_Score as their mean.
5. Saves processed_indices.csv.
"""

import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler

INPUT_FILE = "data/cleaned_data_with_city_filled.csv"  # your current final dataset
OUTPUT_FILE = "data/processed_indices.csv"


# ------------------------------------------------------------
# 1️⃣ Load data
# ------------------------------------------------------------
def load_cleaned_data(path=INPUT_FILE):
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Cleaned data not found: {path}")
    df = pd.read_csv(path, parse_dates=["date"])
    print(f"✅ Loaded {len(df)} cleaned data rows.")
    return df


# ------------------------------------------------------------
# 2️⃣ Compute raw indices
# ------------------------------------------------------------
def compute_raw_indices(df):
    for c in ["PRCP", "TAVG", "AWND", "WSF2", "SNOW", "SNWD"]:
        if c not in df.columns:
            df[c] = 0.0

    # Solar: temperature vs precipitation
    df["Solar_raw"] = df["TAVG"] - (df["PRCP"] / 10.0)

    # Wind: mean of AWND and WSF2
    df["Wind_raw"] = (df["AWND"] + df["WSF2"]) / 2.0

    # Hydro: rainfall + snow
    df["Hydro_raw"] = df["PRCP"].fillna(0) + df["SNOW"].fillna(0) + df["SNWD"].fillna(0)
    return df


# ------------------------------------------------------------
# 3️⃣ Normalize to [0,1]
# ------------------------------------------------------------
def normalize_indices(df):
    scaler = MinMaxScaler()
    for col in ["Solar_raw", "Wind_raw", "Hydro_raw"]:
        norm_col = col.replace("_raw", "")
        df[norm_col] = scaler.fit_transform(df[[col]])
    return df


# ------------------------------------------------------------
# 4️⃣ Combine into Renewable Score
# ------------------------------------------------------------
def compute_combined_score(df):
    df["Renewable_Score"] = df[["Solar", "Wind", "Hydro"]].mean(axis=1)
    return df


# ------------------------------------------------------------
# 5️⃣ Save results
# ------------------------------------------------------------
def save_processed(df, path=OUTPUT_FILE):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"✅ Indexed dataset saved → {path}")


def main():
    df = load_cleaned_data()
    df = compute_raw_indices(df)
    df = normalize_indices(df)
    df = compute_combined_score(df)
    save_processed(df)


if __name__ == "__main__":
    main()
