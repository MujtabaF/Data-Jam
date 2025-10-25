# 🌎 ClimaZoneAI: AI-Driven Renewable Energy Potential Forecasting for Canada

## 🧭 Overview
ClimaZoneAI is an AI-powered analytics platform that forecasts **renewable-energy generation potential** — solar, wind, and hydro — across Canadian cities and provinces.  
Using the **Global Historical Climatology Network (GHCN)** dataset, the platform applies **machine-learning inference and time-series forecasting** to calculate a dynamic **Renewable Energy Index (REI)** for every region.  

Even though many GHCN stations report incomplete weather variables, ClimaZoneAI intelligently reconstructs missing information through **AI-based regression formulas** and **geospatial heuristics** (latitude, longitude, elevation, precipitation), producing accurate, data-driven results.

---

## ⚙️ Methodology

### 1️⃣ Data Source
**Dataset:** Global Historical Climatology Network (GHCN — Canadian subset)  
**Fields used:** station ID, date, observation, value, latitude, longitude, elevation, city, province  
**Available variables:** PRCP, TMAX, TMIN, TAVG, SNOW, SNWD  
**Inferred variables:** AWND, WSF2 (wind metrics), and missing temperature data

---

### 2️⃣ Data Cleaning & AI-Based Inference
Because many daily records contain only one or two variables, ClimaZoneAI reconstructs missing fields through hybrid physical inference and statistical modeling.

| Variable | Inference Logic |
|-----------|----------------|
| **TMIN, TMAX, TAVG** | Derived from elevation, latitude, and seasonal patterns → ΔT = 8 − 0.005 × elevation + 0.1 × month_factor |
| **SNOW, SNWD** | If temperature < 0 °C → convert PRCP to snow (10:1 ratio) |
| **AWND** | 0.2 + 0.004 × elevation + 0.0008 × PRCP + 0.03 × latitude |
| **WSF2** | 1.5 × AWND |

This AI-driven variable reconstruction maintains realistic climate patterns while mitigating missing-data bias.

---

### 3️⃣ Index Calculation
For every record (station-date pair), ClimaZoneAI calculates independent **renewable indices**:

| Index | Formula | Represents |
|--------|----------|------------|
| **Solar Index** | TAVG − PRCP / 10 | Solar favorability (heat vs cloud cover) |
| **Wind Index** | (AWND + WSF2) / 2 | Average and peak wind strength |
| **Hydro Index** | PRCP + SNOW + SNWD | Total precipitation and snow input |

All values are normalized between 0 and 1:
\[
X' = \frac{X - \min(X)}{\max(X) - \min(X)}
\]

The final **Renewable Score**:
\[
REI = \frac{Solar' + Wind' + Hydro'}{3}
\]

This Renewable Energy Index reflects how favorable renewable generation would be on any given day.

---

### 4️⃣ Forecasting Engine
Renewable Score time series for each city are modeled using **Prophet**, enabling forecasts across multiple horizons:

| Forecast Range | Purpose |
|----------------|----------|
| 30 days | Short-term operational planning |
| 4 months | Seasonal adjustment |
| 1 year + | Long-term renewable energy outlook |

For multi-year forecasting, Prophet transitions from seasonality-driven patterns to long-term climate trends.

---

### 5️⃣ Ranking Logic
To identify top-performing renewable cities, ClimaZoneAI aggregates forecast data:

1. Average city-level REI values within each province.  
2. Compute mean forecast scores for the chosen period.  
3. Rank cities to determine top renewable hubs.


---

## 💡 Innovation & AI Highlights
- **AI-Driven Variable Reconstruction:** Fills missing weather data using regression and physics-based inference.  
- **Dynamic Forecasting:** Prophet captures seasonal shifts and long-term non-linear climate behavior.  
- **Cross‑source Integration:** Combines solar, wind, and hydro indices into a single composite REI score.  
- **Geospatial Adaptability:** Produces forecasts for any area, even with minimal station coverage.  
- **Scalability:** Operates on partial datasets, ensuring reliable outputs in remote or rural regions.

---

## 🌐 Visualization & Dashboard
An **interactive dashboard** (Streamlit / Flask + Plotly) enables real‑time filtering and exploration.

**Features**
- Province & city selectors  
- Forecast range: 30 days / 4 months / 1 year / 10 years  
- Predictive charts with confidence intervals  
- Interactive renewable‑potential maps (Folium)  
- Download results in CSV or JSON

---

## 📊 Example Output
| City | Province | Solar | Wind | Hydro | Renewable Score |
|------|-----------|--------|-------|--------|-----------------|
| Nanaimo | BC | 0.62 | 0.41 | 0.68 | 0.57 |
| Kamloops | BC | 0.81 | 0.39 | 0.54 | 0.58 |
| Prince George | BC | 0.44 | 0.48 | 0.79 | 0.57 |

---

## 🧱 Tech Stack
**Languages:** Python  
**Libraries:** Pandas, NumPy, Prophet, Scikit‑learn, Plotly, Matplotlib  
**Framework:** Flask / Streamlit  
**Dataset:** GHCN (Canada‑specific subset)  
**Outputs:** JSON and CSV  

---

## 🏁 Deliverables
| Component | Output |
|------------|---------|
| Data Processing | Cleaned & gap‑filled Canadian dataset |
| AI Inference | Estimated missing weather variables |
| Index Computation | Normalized Solar, Wind, Hydro indices |
| Forecasting Model | Prophet multi‑horizon forecasts |
| Visualization | City and province dashboards |
| Insights | Top 3 renewable cities per province |

---

## 🔮 Future Improvements
- Integrate **ERA5 / NASA POWER** for advanced long-term variables.  
- Add **XGBoost / LSTM hybrid models** for increased predictive accuracy.  
- Simulate energy production efficiency (solar panels, turbines, hydro basins).  

---

## 🏆 Summary
ClimaZoneAI converts incomplete Canadian climate data into **intelligent renewable forecasts**.  
By combining weather data inference, AI‑based modeling, and geospatial forecasting, it identifies the **top 3 renewable cities in every province**, supporting Canada’s **Net‑Zero 2050** targets with data-driven precision.

---

## 👩‍💻 Team
**Team ClimaZoneAI | SFU DataJam 2025**  
Focus: AI for Energy · Sustainable Forecasting · Climate Analytics

