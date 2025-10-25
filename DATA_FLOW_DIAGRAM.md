# ClimaZoneAI - Data Flow Diagram

## Complete Pipeline Visualization

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        DATA ACQUISITION & INPUT                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
        ┌────────────────────────────────────────────────────┐
        │  data/cleaned_data_with_city_filled.csv             │
        │  • Format: Long (observation-based)                 │
        │  • Records: 103,246 rows                            │
        │  • Variables: PRCP, TAVG, SNOW, SNWD, AWND, WSF2   │
        │  • Coverage: 233 Canadian cities                    │
        └────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         DATA TRANSFORMATION                              │
│                      src/compute_indices.py (Step 1)                     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                ▼                   ▼                   ▼
        ┌───────────────┐   ┌──────────────┐   ┌──────────────┐
        │ Pivot Table   │   │ Add Province │   │ Handle NaN   │
        │ Long → Wide   │   │ Column       │   │ Fill Values  │
        └───────────────┘   └──────────────┘   └──────────────┘
                │                   │                   │
                └───────────────────┼───────────────────┘
                                    ▼
        ┌────────────────────────────────────────────────────┐
        │  data/processed_wide_format.csv                     │
        │  • Format: Wide (station-date based)                │
        │  • Records: 95,848 rows                             │
        │  • Columns: 17 (station, date, weather vars)        │
        └────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        FEATURE ENGINEERING                               │
│                      src/compute_indices.py (Step 2)                     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ Monthly          │     │ Solar Index      │     │ Wind Index       │
│ Aggregation      │     │                  │     │                  │
│                  │     │ Solar_raw =      │     │ Wind_raw =       │
│ Group by:        │     │ TAVG -           │     │ (AWND + WSF2)    │
│ city + month     │     │ (PRCP / 10)      │     │ / 2.0            │
│                  │     │                  │     │                  │
│ Sum: PRCP, SNOW  │     │ Higher temp =    │     │ Avg wind +       │
│ Mean: SNWD       │     │ Better solar     │     │ gusts            │
└──────────────────┘     └──────────────────┘     └──────────────────┘
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    ▼
                        ┌──────────────────────┐
                        │ Hydro Index          │
                        │                      │
                        │ Hydro_raw =          │
                        │ (monthly_PRCP × 2.0) │
                        │ + (monthly_SNOW×1.5) │
                        │ + (monthly_SNWD×0.5) │
                        │                      │
                        │ Cumulative water     │
                        │ resources            │
                        └──────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         NORMALIZATION                                    │
│              Percentile-Based Robust Scaling                             │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ Solar Index      │     │ Wind Index       │     │ Hydro Index      │
│                  │     │                  │     │                  │
│ p5 = 5th %ile    │     │ p5 = 5th %ile    │     │ p5 = 5th %ile    │
│ p95 = 95th %ile  │     │ p95 = 95th %ile  │     │ p95 = 95th %ile  │
│                  │     │                  │     │                  │
│ Normalized =     │     │ Normalized =     │     │ Normalized =     │
│ (value - p5) /   │     │ (value - p5) /   │     │ (value - p5) /   │
│ (p95 - p5)       │     │ (p95 - p5)       │     │ (p95 - p5)       │
│                  │     │                  │     │                  │
│ Range: [0, 1]    │     │ Range: [0, 1]    │     │ Range: [0, 1]    │
│ Mean: 0.435      │     │ Mean: 0.297      │     │ Mean: 0.229      │
└──────────────────┘     └──────────────────┘     └──────────────────┘
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    ▼
                        ┌──────────────────────┐
                        │ Renewable Score      │
                        │                      │
                        │ Combined =           │
                        │ (Solar + Wind +      │
                        │  Hydro) / 3          │
                        │                      │
                        │ Range: [0, 1]        │
                        └──────────────────────┘
                                    │
                                    ▼
        ┌────────────────────────────────────────────────────┐
        │  data/processed_indices.csv                         │
        │  • Records: 95,848 rows                             │
        │  • Indices: Solar, Wind, Hydro, Renewable_Score     │
        │  • Ready for forecasting & visualization            │
        └────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        FORECASTING ENGINE                                │
│                  generate_html_dashboard.py                              │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                ▼                   ▼                   ▼
        ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
        │ 30 Days      │   │ 4 Months     │   │ 1 Year       │
        │              │   │              │   │              │
        │ Daily        │   │ Monthly      │   │ Monthly      │
        │ predictions  │   │ aggregated   │   │ aggregated   │
        │              │   │              │   │              │
        │ 30 points    │   │ 4 points     │   │ 12 points    │
        └──────────────┘   └──────────────┘   └──────────────┘
                │                   │                   │
                └───────────────────┼───────────────────┘
                                    ▼
                        ┌──────────────────────┐
                        │ Pattern Matching     │
                        │                      │
                        │ For each future date:│
                        │ 1. Get month number  │
                        │ 2. Look up historical│
                        │    monthly average   │
                        │ 3. Apply pattern     │
                        │                      │
                        │ Seasonal accuracy ✓  │
                        └──────────────────────┘
                                    │
                                    ▼
        ┌────────────────────────────────────────────────────┐
        │  Forecast Data (JSON)                               │
        │  • 232 cities × 3 time horizons                     │
        │  • All indices pre-computed                         │
        │  • Embedded in HTML dashboard                       │
        └────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        VISUALIZATION LAYER                               │
│                         web/dashboard.html                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ Chart 1:         │     │ Chart 2:         │     │ Chart 3:         │
│ Energy Type      │     │ Overall Score    │     │ Energy Breakdown │
│ Comparison       │     │                  │     │                  │
│                  │     │ • Area chart     │     │ • Grouped bars   │
│ • 3 lines        │     │ • Renewable      │     │ • Monthly        │
│ • Solar (orange) │     │   Score trend    │     │   comparison     │
│ • Wind (blue)    │     │ • Fill to zero   │     │ • Side-by-side   │
│ • Hydro (teal)   │     │ • Green gradient │     │ • All 3 types    │
│                  │     │                  │     │                  │
│ connectgaps:false│     │ connectgaps:false│     │ No gaps in bars  │
└──────────────────┘     └──────────────────┘     └──────────────────┘
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    ▼
                        ┌──────────────────────┐
                        │ Interactive Controls │
                        │                      │
                        │ 📍 Province dropdown │
                        │ 🏙️ City dropdown     │
                        │ 🔮 Forecast period   │
                        │    (30d/4m/1y)       │
                        │                      │
                        │ ⚡ Real-time update   │
                        └──────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE                                 │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ Metrics Cards    │     │ Chart Interaction│     │ Responsive Design│
│                  │     │                  │     │                  │
│ ☀️ Solar: 0.44   │     │ • Hover details  │     │ • Desktop ✓      │
│ 💨 Wind: 0.30    │     │ • Zoom/pan       │     │ • Tablet ✓       │
│ 💧 Hydro: 0.23   │     │ • Export image   │     │ • Mobile ✓       │
│ 🌍 Overall: 0.32 │     │ • Toggle traces  │     │ • No server ✓    │
└──────────────────┘     └──────────────────┘     └──────────────────┘


═══════════════════════════════════════════════════════════════════════════
                           GAP HANDLING FLOW
═══════════════════════════════════════════════════════════════════════════

        ┌────────────────────────────────────────────────────┐
        │ Raw Monthly Data                                    │
        │ (Some months may have gaps)                         │
        └────────────────────────────────────────────────────┘
                                    │
                                    ▼
        ┌────────────────────────────────────────────────────┐
        │ Step 1: Count Data Points per Month                │
        │ • Group by city + month                             │
        │ • Count number of daily records                     │
        └────────────────────────────────────────────────────┘
                                    │
                                    ▼
        ┌────────────────────────────────────────────────────┐
        │ Step 2: Filter Insufficient Data                    │
        │ • Require minimum 3 days per month                  │
        │ • Remove months with < 3 data points                │
        │ • Rationale: Unreliable averages                    │
        └────────────────────────────────────────────────────┘
                                    │
                                    ▼
        ┌────────────────────────────────────────────────────┐
        │ Step 3: Remove NaN Values                           │
        │ • Drop rows with any missing indices                │
        │ • Ensure complete data for visualization            │
        └────────────────────────────────────────────────────┘
                                    │
                                    ▼
        ┌────────────────────────────────────────────────────┐
        │ Step 4: Plotly Configuration                        │
        │ • connectgaps: false                                │
        │ • line: { shape: 'linear' }                         │
        │ • No artificial interpolation                       │
        └────────────────────────────────────────────────────┘
                                    │
                                    ▼
        ┌────────────────────────────────────────────────────┐
        │ Result: Honest Visualization                        │
        │                                                     │
        │ Vancouver (complete):                               │
        │ • ── • ── • ── • ── • ── •                          │
        │                                                     │
        │ Cranbrook (sparse):                                 │
        │ •        [gap]        •        [gap]        •       │
        │                                                     │
        │ User sees real data quality ✓                       │
        └────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════
                    DATA STATISTICS AT EACH STAGE
═══════════════════════════════════════════════════════════════════════════

Input (Long Format):
├─ Records: 103,246
├─ Cities: 233
├─ Time Range: 2022-2024
└─ Observations: PRCP, TAVG, SNOW, SNWD, AWND, WSF2, TMAX, TMIN

After Transformation (Wide Format):
├─ Records: 95,848 (-7%)
├─ Cities: 233
├─ Columns: 17
└─ Reason for reduction: Incomplete station-date pairs

After Index Calculation:
├─ Records: 95,848
├─ Cities: 232 (-1 removed for insufficient data)
├─ New Columns: Solar, Wind, Hydro, Renewable_Score
├─ Solar Mean: 0.435, Median: 0.422
├─ Wind Mean: 0.297, Median: 0.171
└─ Hydro Mean: 0.229, Median: 0.106

After Monthly Aggregation (Dashboard):
├─ Total City-Month Combinations: ~5,500
├─ Filtered (≥3 days): ~5,200 (-5%)
├─ With Complete Indices: ~4,800 (-13%)
└─ Final Dashboard Cities: 232

Forecast Generation:
├─ Cities with Forecasts: 232
├─ Time Horizons: 3 (30d, 4m, 1y)
├─ Total Forecast Points: ~15,000
└─ Forecast Method: Historical pattern replication
```

## Key Pipeline Decisions

### Why Long → Wide Format?

- **Efficiency:** Wide format enables vectorized operations
- **Compatibility:** Machine learning models expect feature columns
- **Clarity:** One row per observation vs. multiple rows

### Why Monthly Aggregation for Hydro?

- **Reality:** Hydro power uses accumulated water, not daily rain
- **Infrastructure:** Reservoirs store water over time
- **Accuracy:** Better reflects Canada's hydro capacity (60% of electricity)

### Why Percentile-Based Normalization?

- **Robustness:** Outliers don't distort the scale
- **Balance:** All three indices equally visible
- **Interpretability:** 0 = low potential, 1 = high potential

### Why Pattern-Based Forecasting?

- **Seasonality:** Renewable energy follows strong seasonal cycles
- **Simplicity:** Easy to understand and validate
- **Speed:** No model training required for HTML dashboard
- **Portability:** Works in static HTML (no Python backend)

### Why Disable `connectgaps`?

- **Honesty:** Shows real data quality
- **Trust:** No artificial smoothing
- **Scientific Integrity:** Gaps indicate missing measurements, not zero values

---

**This diagram represents the complete end-to-end pipeline from raw CSV data to interactive forecasting dashboard.**
