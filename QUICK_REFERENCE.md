# ClimaZoneAI - Quick Reference Summary

## 📊 Project Overview

**What:** AI-powered renewable energy forecasting system for Canada  
**Data Source:** GHCN (Global Historical Climatology Network) weather data  
**Coverage:** 232 Canadian cities across 13 provinces/territories  
**Output:** Interactive HTML dashboard with 30-day, 4-month, and 1-year forecasts

---

## 🔄 Pipeline Summary (5 Steps)

```
CSV Data → Transform → Calculate Indices → Forecast → Visualize
```

### 1. **Data Loading** 📥

- **Input:** `cleaned_data_with_city_filled.csv` (103K rows)
- **Format:** Long format (observation-based)
- **Variables:** PRCP, TAVG, SNOW, SNWD, AWND, WSF2

### 2. **Data Transformation** 🔄

- **Process:** Long → Wide format conversion
- **Output:** `processed_wide_format.csv` (96K rows × 17 cols)
- **Features:** Add province, fill missing values

### 3. **Index Calculation** 📐

- **Solar:** `TAVG - (PRCP/10)` → Normalized [0,1]
- **Wind:** `(AWND + WSF2) / 2` → Normalized [0,1]
- **Hydro:** `(monthly_PRCP×2) + (monthly_SNOW×1.5) + (monthly_SNWD×0.5)` → Normalized [0,1]
- **Combined:** `(Solar + Wind + Hydro) / 3`
- **Normalization:** Percentile-based (5th-95th) for robustness

### 4. **Forecasting** 🔮

- **Method:** Historical monthly pattern replication
- **Logic:** Future month X gets average of all historical month X values
- **Horizons:** 30 days (daily), 4 months (monthly), 1 year (monthly)

### 5. **Visualization** 📈

- **Tech:** Static HTML + Plotly.js (no server required)
- **Charts:** 3 interactive charts + 4 metric cards
- **Features:** Province/city/period selectors
- **Gap Handling:** `connectgaps: false` for honest visualization

---

## 💡 Key Technical Decisions

### Why Monthly Hydro Aggregation?

- **Problem:** 88% of days have zero precipitation
- **Reality:** Hydro uses accumulated water (reservoirs)
- **Solution:** Calculate total monthly precipitation per city
- **Result:** Hydro mean increased from 0.01 → 0.23 (reflects Canada's 60% hydro capacity)

### Why Percentile Normalization?

- **Problem:** Min-max scaling sensitive to outliers
- **Solution:** Use 5th-95th percentile bounds
- **Benefit:** More balanced distribution across all indices

### Why Gap Handling?

- **Problem:** Not all cities have complete monthly data
- **Bad:** Connect lines across gaps → misleading trends
- **Good:** Break lines at gaps → honest representation
- **Implementation:** `connectgaps: false` + filter months with <3 days

---

## 📈 Results at a Glance

### Index Statistics

| Index | Mean  | Median | Interpretation                   |
| ----- | ----- | ------ | -------------------------------- |
| Solar | 0.435 | 0.422  | Good potential across Canada     |
| Wind  | 0.297 | 0.171  | Moderate, varies by region       |
| Hydro | 0.229 | 0.106  | Concentrated in specific regions |

### Geographic Leaders

- **Hydro:** BC (mountains), QC (rivers), MB (lakes)
- **Wind:** AB (prairies), SK (plains), NL (coast)
- **Solar:** ON (south), AB (clear), SK (long days)

### Seasonal Patterns

- **Spring:** ⬆️ Hydro (snowmelt), ⬆️ Wind, → Solar
- **Summer:** ⬆️⬆️ Solar, ⬇️ Wind, ⬇️ Hydro
- **Fall:** ⬆️ Wind (storms), ⬇️ Solar, ⬆️ Hydro (rain)
- **Winter:** ⬇️⬇️ Solar, ⬆️ Wind, → Hydro (frozen)

---

## 🛠️ Tech Stack

**Backend (Python):**

- pandas, numpy (data processing)
- scikit-learn (normalization)
- prophet, xgboost (advanced models - Streamlit only)

**Frontend (HTML Dashboard):**

- Plotly.js (interactive charts)
- Vanilla JavaScript (no frameworks)
- CSS3 (responsive design)

---

## 📁 File Structure

```
Data-Jam/
├── data/
│   ├── cleaned_data_with_city_filled.csv     [INPUT]
│   ├── processed_wide_format.csv             [STEP 1]
│   └── processed_indices.csv                 [STEP 2]
├── src/
│   └── compute_indices.py                    [PROCESSING]
├── generate_html_dashboard.py                [FORECASTING]
└── web/
    └── dashboard.html                        [OUTPUT]
```

---

## 🎯 Usage

### Generate Dashboard:

```bash
# Step 1: Calculate indices
python3 src/compute_indices.py

# Step 2: Generate dashboard
python3 generate_html_dashboard.py

# Step 3: Open dashboard
open web/dashboard.html
```

### Use Dashboard:

1. Select **Province** (e.g., British Columbia)
2. Select **City** (e.g., Vancouver)
3. Select **Forecast Period** (30d / 4m / 1y)
4. View **3 charts** + **4 metrics**

---

## 🎨 Dashboard Features

### Interactive Controls

- 📍 **13 provinces/territories**
- 🏙️ **232 cities**
- 🔮 **3 forecast periods**

### Chart Types

1. **Energy Type Comparison** - 3 lines (Solar, Wind, Hydro)
2. **Overall Score Trend** - Area chart with fill
3. **Energy Breakdown** - Grouped bar chart

### Metrics Cards

- ☀️ Solar Index (avg)
- 💨 Wind Index (avg)
- 💧 Hydro Index (avg)
- 🌍 Overall Score (avg)

---

## 🚀 Deployment Options

- ✅ **GitHub Pages** (free hosting)
- ✅ **Netlify** (drag & drop)
- ✅ **Local File** (open in browser)
- ✅ **USB Drive** (portable demo)
- ✅ **Email** (send HTML file)

**No server, no backend, no installation required!**

---

## 📊 Model Comparison

| Model             | Used In        | Strengths                      | Limitations               |
| ----------------- | -------------- | ------------------------------ | ------------------------- |
| **Pattern-Based** | HTML Dashboard | Fast, portable, seasonal       | No trend learning         |
| **Prophet**       | Streamlit App  | Trend + seasonality, CI        | Needs Python backend      |
| **XGBoost**       | Streamlit App  | Non-linear, feature importance | Complex, overfitting risk |
| **Ensemble**      | Streamlit App  | Best accuracy                  | Computational overhead    |

---

## 🎤 Presentation Talking Points

### 1. Problem Statement (30 sec)

"Canada has diverse climate zones. Where should we invest in renewable energy? We need data-driven predictions."

### 2. Solution Overview (30 sec)

"ClimaZoneAI analyzes historical weather data to forecast solar, wind, and hydro potential across 232 Canadian cities with interactive visualizations."

### 3. Technical Highlights (60 sec)

- **Smart Hydro Calculation:** Monthly aggregation reflects real infrastructure
- **Robust Normalization:** Percentile-based to handle outliers
- **Honest Gaps:** No artificial smoothing, shows real data quality
- **Multiple Horizons:** 30 days, 4 months, 1 year

### 4. Demo (90 sec)

- Show Vancouver (complete data): "Smooth lines, high hydro"
- Show Cranbrook (sparse data): "Gaps visible, honest representation"
- Switch periods: "30 days → 4 months → 1 year"
- Compare provinces: "BC has hydro, AB has wind"

### 5. Impact (30 sec)

"Helps energy planners make informed decisions. Identifies best locations for solar farms, wind turbines, and hydro upgrades. Supports Canada's renewable energy transition."

---

## 🏆 Unique Selling Points

1. **Realistic Hydro Model** - Monthly aggregation (not daily)
2. **Transparent Visualization** - Shows data gaps honestly
3. **No Server Required** - Pure HTML deployment
4. **Multiple Time Scales** - Short-term and long-term planning
5. **Comprehensive Coverage** - 232 cities, all provinces

---

## 📞 Contact & Resources

**Report:** `TECHNICAL_REPORT.md` (detailed methodology)  
**Diagram:** `DATA_FLOW_DIAGRAM.md` (visual pipeline)  
**Dashboard:** `web/dashboard.html` (live demo)  
**Code:** GitHub repository

**Team ClimaZoneAI | SFU DataJam 2025**

---

## 🔑 Key Formulas (For Reference)

**Solar Index:**

```
Solar_raw = TAVG - (PRCP / 10.0)
Solar = (Solar_raw.clip(p5, p95) - p5) / (p95 - p5)
```

**Wind Index:**

```
Wind_raw = (AWND + WSF2) / 2.0
Wind = (Wind_raw.clip(p5, p95) - p5) / (p95 - p5)
```

**Hydro Index:**

```
Hydro_raw = (monthly_PRCP × 2.0) + (monthly_SNOW × 1.5) + (monthly_SNWD × 0.5)
Hydro = (Hydro_raw.clip(p5, p95) - p5) / (p95 - p5)
```

**Renewable Score:**

```
Renewable_Score = (Solar + Wind + Hydro) / 3.0
```

**Forecast:**

```
For date D in future:
    month = D.month
    forecast[D] = historical_monthly_avg[month]
```
