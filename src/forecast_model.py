"""
ClimaZoneAI — Forecasting Module
--------------------------------
1. Loads processed dataset (with Solar, Wind, Hydro, Renewable_Score)
2. Groups by City/Province
3. Runs Prophet forecast for next 30 days, 4 months, and 1 year
4. Falls back to linear regression if Prophet isn't installed
5. Saves forecast_results.csv with predictions

Author: ClimaZoneAI Team
Version: 2.0
"""

import pandas as pd
import numpy as np
import os
from datetime import timedelta

# Try to import Prophet
try:
    from prophet import Prophet
    USE_PROPHET = True
except ImportError:
    from sklearn.linear_model import LinearRegression
    USE_PROPHET = False
    print("⚠️ Prophet not found — using Linear Regression fallback.")

# === File paths ===
INPUT_FILE = "data/processed_indices.csv"
OUTPUT_FILE = "data/forecast_results.csv"


# ------------------------------------------------------------
# 1️⃣ Load processed data
# ------------------------------------------------------------
def load_processed_data(path=INPUT_FILE):
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Processed data not found: {path}")
    df = pd.read_csv(path, parse_dates=["date"], low_memory=False)
    print(f"✅ Loaded {len(df)} rows from {path}")
    return df


# ------------------------------------------------------------
# 2️⃣ Forecasting logic (Prophet)
# ------------------------------------------------------------
def prophet_forecast(df, days_ahead=30):
    """Runs Prophet forecast for Renewable_Score."""
    model_df = df.rename(columns={"date": "ds", "Renewable_Score": "y"})
    model = Prophet(daily_seasonality=False, yearly_seasonality=True)
    model.fit(model_df)
    future = model.make_future_dataframe(periods=days_ahead)
    forecast = model.predict(future)
    return forecast[["ds", "yhat"]].rename(columns={"ds": "date", "yhat": "forecast"})


# ------------------------------------------------------------
# 3️⃣ Forecasting logic (Linear Regression fallback)
# ------------------------------------------------------------
def linear_forecast(df, days_ahead=30):
    """Linear trend-based fallback if Prophet not available."""
    df = df.dropna(subset=["Renewable_Score"])
    df = df.sort_values("date")
    df["t"] = (df["date"] - df["date"].min()).dt.days
    X, y = df[["t"]], df["Renewable_Score"]
    model = LinearRegression().fit(X, y)

    future_dates = pd.date_range(df["date"].max() + timedelta(days=1), periods=days_ahead)
    t_future = (future_dates - df["date"].min()).days.values.reshape(-1, 1)
    y_future = model.predict(t_future)
    forecast = pd.DataFrame({"date": future_dates, "forecast": y_future})
    return forecast


# ------------------------------------------------------------
# 4️⃣ Forecast each city/province
# ------------------------------------------------------------
def forecast_all(df, forecast_days=30):
    """Run forecasts for each city (and optionally province)."""
    results = []
    groups = df.groupby(["province", "city"], dropna=False)

    for (prov, city), group in groups:
        try:
            group = group.sort_values("date")
            if len(group) < 10:
                continue

            forecast = (prophet_forecast(group, forecast_days)
                        if USE_PROPHET else linear_forecast(group, forecast_days))
            forecast["province"] = prov
            forecast["city"] = city
            results.append(forecast)
        except Exception as e:
            print(f"⚠️ Forecast failed for {city}, {prov}: {e}")
            continue

    all_forecasts = pd.concat(results, ignore_index=True)
    print(f"✅ Forecasts generated for {len(all_forecasts['city'].unique())} cities.")
    return all_forecasts


# ------------------------------------------------------------
# 5️⃣ Save results
# ------------------------------------------------------------
def save_forecast(df, path=OUTPUT_FILE):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"✅ Forecast results saved → {path}")


# ------------------------------------------------------------
# 6️⃣ Main
# ------------------------------------------------------------
def main():
    df = load_processed_data()

    # Generate 3 forecast sets
    forecast_30 = forecast_all(df, 30)
    forecast_120 = forecast_all(df, 120)
    forecast_365 = forecast_all(df, 365)

    # Add time horizon tags
    forecast_30["period"] = "30_days"
    forecast_120["period"] = "4_months"
    forecast_365["period"] = "1_year"

    # Combine all results
    combined = pd.concat([forecast_30, forecast_120, forecast_365])
    save_forecast(combined)


if __name__ == "__main__":
    main()
