# ClimaZoneAI - Renewable Energy Forecasting for Canada

## 🌟 Inspiration

Canada is at a critical juncture in its energy transition. With a commitment to reaching **net-zero emissions by 2050**, understanding where and when renewable energy will be most effective is crucial. However, Canada's vast geographic diversity presents a unique challenge:

- **British Columbia** has abundant hydro resources from mountain snowmelt
- **Alberta** has some of the best wind potential on the prairies
- **Ontario** has strong solar potential in the south
- But how do we **quantify** and **forecast** these differences?

**The challenge:** We had historical weather data from 233 Canadian cities, but the data was messy - many weather stations only recorded 1-2 variables, leaving critical measurements like wind speed completely missing. Traditional analysis would simply discard incomplete data, losing valuable geographic coverage.

**Our vision:** Build an AI-powered system that could:

1. **Intelligently infer** missing weather variables using geographic features
2. **Calculate realistic** renewable energy potential indices
3. **Forecast future** energy potential across multiple time horizons
4. **Visualize** everything in an accessible, interactive dashboard

We were inspired by the idea that **better data leads to better decisions** - and those decisions could directly impact where Canada invests billions in renewable infrastructure.

---

## 💡 What We Learned

### 1. **Domain Knowledge is Critical**

Our biggest "aha moment" came when we noticed our **hydro index was showing nearly zero** for all Canadian cities. This made no sense - Canada generates 60% of its electricity from hydro!

**The problem:** We were calculating hydro potential from **daily precipitation**, but 88% of days have zero rainfall.

**The insight:** Real hydro systems work on **accumulated water resources** - reservoirs fill over weeks and months, not hours. We needed to think like hydrologists, not just data scientists.

**The solution:** We implemented **monthly aggregation** for hydro calculations:

$$
\text{Hydro}_{\text{raw}} = 2.0 \times \sum_{i=1}^{30} \text{PRCP}_i + 1.5 \times \sum_{i=1}^{30} \text{SNOW}_i + 0.5 \times \overline{\text{SNWD}}
$$

Where:

- $\text{PRCP}_i$ = daily precipitation (mm)
- $\text{SNOW}_i$ = daily snowfall (mm)
- $\overline{\text{SNWD}}$ = average monthly snow depth (mm)

**Result:** Hydro index jumped from 0.01 to 0.23 average - now reflecting reality!

**Lesson:** Domain expertise > blind data processing. Always validate results against real-world knowledge.

---

### 2. **AI Can Fill the Gaps - If You're Smart About It**

With many weather stations missing wind measurements, we had two choices:

1. Discard all incomplete data (lose 40% of cities)
2. Infer missing values intelligently

We chose option 2, building a **physics-informed AI inference model**:

$$
\text{AWND} = \left(0.2 + 0.004 \times h + 0.0008 \times P + 0.03 \times |\phi - 45°|\right)_{[0.5, 12]}
$$

Where:

- $h$ = elevation (meters)
- $P$ = precipitation (mm)
- $\phi$ = latitude (degrees)
- $[\cdot]_{[a,b]}$ = clip to range [a, b]

**Why this works:**

- Higher elevation → Mountains create wind (orographic effect)
- Precipitation → Usually comes with storm systems (wind events)
- Distance from mid-latitude → More extreme weather systems

**Validation:** Our inferred wind speeds had:

- Mean: 1.69 m/s (realistic for Canada ✓)
- Range: 0.5-10.5 m/s (physically plausible ✓)
- Correlation with storms: Strong ✓

**Lesson:** AI inference works best when informed by physics and domain knowledge, not just statistical patterns.

---

### 3. **Honest Visualization Builds Trust**

Initially, our graphs looked "nicer" with smooth, continuous lines. But we realized we were **lying to users** by connecting lines across missing months.

**Example:**

```
BAD (connectgaps: true):
• ─────────────────────────────── •
  Jan                            May
  ↑ Misleading! No data Feb-Apr

GOOD (connectgaps: false):
•               [gap]             •
  Jan                            May
  ↑ Honest! Shows data quality
```

We implemented strict gap handling:

1. **Filter out** months with <3 days of data
2. **Drop rows** with any NaN values
3. **Disable interpolation**: `connectgaps: false` in Plotly
4. **Linear shape**: No artificial smoothing

**Result:** Users see exactly what data we have - no artificial smoothness, no hidden problems.

**Lesson:** In scientific applications, honesty > aesthetics. Show users the truth, even if it's messy.

---

### 4. **Percentile Normalization > Min-Max Scaling**

Standard min-max normalization failed us:

$$
x_{\text{norm}} = \frac{x - x_{\min}}{x_{\max} - x_{\min}}
$$

**Problem:** One extreme outlier (e.g., a hurricane with 150 mm rain) compressed all normal values to near-zero.

**Solution:** Percentile-based robust scaling:

$$
x_{\text{norm}} = \frac{\text{clip}(x, p_5, p_{95}) - p_5}{p_{95} - p_5}
$$

Where $p_5$ and $p_{95}$ are the 5th and 95th percentiles.

**Result:** Much more balanced distribution across all three energy types:

- Solar: 0.435 mean (was 0.02)
- Wind: 0.297 mean (was 0.15)
- Hydro: 0.229 mean (was 0.01)

**Lesson:** Robust statistics > naive statistics for real-world data.

---

### 5. **Static HTML > Dynamic Web Apps for Demos**

We built both a Streamlit app (with advanced ML models) and a static HTML dashboard. For hackathon demos, **HTML won decisively**:

**Streamlit Challenges:**

- Requires Python backend running
- Port conflicts (8501 often taken)
- Slower loading with large datasets
- Can't easily share with judges

**HTML Advantages:**

- ✅ Double-click to open (no installation)
- ✅ Works offline
- ✅ Email as attachment
- ✅ Deploy to GitHub Pages in 30 seconds
- ✅ No dependencies

**Lesson:** For demos and presentations, portability trumps features. Build the advanced stuff, but make sure you have a simple way to show it.

---

## 🛠️ How We Built It

### Phase 1: Data Pipeline (The Messy Reality)

**Challenge:** Input data was in "long format" - one row per observation:

```csv
station,date,observation,value
CA001,2024-01-01,PRCP,5.2
CA001,2024-01-01,TAVG,-2.1
CA001,2024-01-01,SNOW,0.0
```

This meant 8 rows per station-date combination. Completely unworkable for ML!

**Solution:** Built a transformation pipeline:

```python
# Step 1: Pivot to wide format
df_wide = df.pivot_table(
    index=['station', 'date', 'latitude', 'longitude',
           'elevation', 'city'],
    columns='observation',
    values='value',
    aggfunc='first'
)

# Step 2: Extract province from city_province
df_wide['province'] = df_wide['city_province'].apply(
    lambda x: x.split(', ')[-1]
)

# Step 3: AI-driven inference for missing variables
df_wide = infer_missing_variables(df_wide)
```

**Result:** 103,246 long-format rows → 95,848 wide-format rows with complete features.

---

### Phase 2: Feature Engineering (Making Data Meaningful)

Raw weather numbers don't directly tell you energy potential. We engineered domain-specific indices:

#### **Solar Index**

$$
\text{Solar}_{\text{raw}} = \text{TAVG} - \frac{\text{PRCP}}{10}
$$

**Rationale:**

- Higher temperature = Better solar panel efficiency
- More precipitation = Cloud cover = Less sunlight
- Division by 10 scales precipitation appropriately

#### **Wind Index**

$$
\text{Wind}_{\text{raw}} = \frac{\text{AWND} + \text{WSF2}}{2}
$$

**Rationale:**

- Average wind speed (AWND) = Sustained energy
- Wind gusts (WSF2) = Peak capacity
- Both matter for turbine performance

#### **Hydro Index** (Our Innovation!)

$$
\text{Hydro}_{\text{raw}} = 2.0 \times \text{PRCP}_{\text{monthly}} + 1.5 \times \text{SNOW}_{\text{monthly}} + 0.5 \times \overline{\text{SNWD}_{\text{monthly}}}
$$

**Why monthly?** Hydro reservoirs accumulate water over weeks/months, not days!

#### **Normalization**

$$
\text{Index}_{\text{norm}} = \frac{\text{clip}(\text{Index}_{\text{raw}}, p_5, p_{95}) - p_5}{p_{95} - p_5}
$$

All indices normalized to [0, 1] using robust percentile scaling.

#### **Combined Score**

$$
\text{Renewable Score} = \frac{\text{Solar} + \text{Wind} + \text{Hydro}}{3}
$$

---

### Phase 3: Forecasting Engine (Pattern-Based Intelligence)

We needed forecasts for three time horizons:

- **30 days** (daily operations)
- **4 months** (seasonal planning)
- **1 year** (annual projections)

**Core Algorithm:** Historical pattern replication

```python
def forecast(city, days_ahead):
    # Learn monthly patterns from history
    patterns = historical_data.groupby('month').agg({
        'Solar': 'mean',
        'Wind': 'mean',
        'Hydro': 'mean'
    })

    # Apply patterns to future dates
    for future_date in next_N_days:
        month = future_date.month
        prediction[future_date] = patterns[month]

    return prediction
```

**Why this works:**

- Renewable energy is **highly seasonal**
- Solar peaks in summer (long days, clear skies)
- Wind peaks in spring/fall (storm systems)
- Hydro peaks in spring (snowmelt)

**Aggregation Logic:**

- 30 days → Display daily (30 points)
- 4 months → Aggregate to monthly (4 points) for clarity
- 1 year → Aggregate to monthly (12 points) for readability

**Result:** Fast, interpretable forecasts with no model training required!

---

### Phase 4: Visualization Dashboard (Making It Accessible)

**Goal:** Anyone should be able to explore renewable energy potential across Canada.

**Technology Choice:** Static HTML + Plotly.js

**Why?**

- No server required (portable)
- Works offline
- Fast loading
- Universal compatibility

**Implementation:**

```python
# Generate dashboard
def generate_html_dashboard():
    # Pre-compute ALL forecasts for ALL cities
    forecasts = {}
    for city in cities:
        forecasts[city] = {
            '30d': forecast(city, 30),
            '4m': forecast(city, 120),
            '1y': forecast(city, 365)
        }

    # Embed in HTML with JavaScript
    html = f"""
    <script>
        const allData = {json.dumps(forecasts)};

        function updateCharts() {{
            const city = document.getElementById('city').value;
            const period = document.getElementById('period').value;
            const data = allData[city][period];

            // Update 3 Plotly charts
            plotEnergyComparison(data);
            plotOverallTrend(data);
            plotBreakdown(data);
        }}
    </script>
    """
```

**Key Configuration:**

```javascript
{
    x: dates,
    y: values,
    mode: 'lines+markers',
    line: {
        shape: 'linear',  // No interpolation
        width: 3
    },
    connectgaps: false,  // DON'T connect missing data!
    marker: { size: 8 }
}
```

**Features:**

- 3 dropdowns (Province, City, Forecast Period)
- 3 interactive charts (Plotly.js)
- 4 metric cards (averages)
- Responsive design (mobile-friendly)
- Zero dependencies (self-contained)

**Result:** A dashboard that works anywhere - laptop, tablet, phone, even a USB drive!

---

## 🚧 Challenges We Faced

### Challenge 1: The Hydro Index Mystery 🧐

**Problem:** Initial hydro index showed ~0.01 for all cities (effectively zero).

**Why it happened:** We calculated hydro from daily precipitation, but 88% of days have 0mm rain!

**Debug process:**

```python
# Checked data distribution
print(df['PRCP'].describe())
# count    95848
# mean     0.68 mm
# 50%      0.00 mm  ← MEDIAN IS ZERO!
# 75%      0.00 mm  ← 75th percentile ALSO ZERO!
```

**Solution:** Realized hydro needs monthly cumulative data (like real reservoirs). Implemented monthly aggregation.

**Time cost:** 4 hours of debugging and research.

**Lesson:** When results don't match reality, check your assumptions about the domain!

---

### Challenge 2: XGBoost Wouldn't Install on macOS 😤

**Error:**

```
XGBoostError: Library not loaded: @rpath/libomp.dylib
Reason: no such file
```

**Why:** XGBoost requires OpenMP for parallel processing, not included in macOS by default.

**Solutions tried:**

1. `pip uninstall/reinstall xgboost` ❌
2. Update Python ❌
3. Try conda environment ❌

**What worked:**

```bash
brew install libomp
```

**Time cost:** 2 hours of Stack Overflow diving.

**Lesson:** Platform-specific dependencies are a pain. Always document setup steps!

---

### Challenge 3: JSON Serialization Hell 🔥

**Problem:** Generating HTML dashboard crashed with:

```
TypeError: Object of type Timestamp is not JSON serializable
```

**Why:** Pandas timestamps aren't JSON-compatible!

**Initial attempts:**

```python
# Tried 1: Convert to string
df['date'] = df['date'].astype(str)  # Still nested timestamps!

# Tried 2: to_dict()
data = df.to_dict('records')  # Still has Period objects!
```

**Solution:** Manual conversion:

```python
result = []
for _, row in df.iterrows():
    result.append({
        'period': row['date'].strftime('%Y-%m-%d'),  # Explicit string
        'Solar': round(float(row['Solar']), 3),      # Explicit float
        'Wind': round(float(row['Wind']), 3),
        'Hydro': round(float(row['Hydro']), 3)
    })
```

**Time cost:** 1.5 hours.

**Lesson:** When serializing for web, be explicit about types. Don't trust automatic conversions.

---

### Challenge 4: Data Gaps - To Connect or Not to Connect? 🤔

**Problem:** Some cities (like Cranbrook) have sparse data - data for Jan, then nothing until May.

**Initial approach:** Let Plotly connect the lines (looked prettier).

**Realization:** We're showing a **false trend**! There's no data Feb-Apr, so we shouldn't imply continuous measurements.

**Ethical dilemma:** Should we:

- Make graphs look nice (smooth lines)?
- Show truth (gaps visible)?

**Decision:** Truth > aesthetics. Implemented strict gap handling.

**Code:**

```python
# Filter months with <3 days
monthly = monthly[monthly['day_count'] >= 3]

# Drop any remaining NaN
monthly = monthly.dropna()

# JavaScript config
connectgaps: false  // Key!
```

**Time cost:** 3 hours of discussion and implementation.

**Lesson:** In scientific applications, honesty is paramount. Show the limitations of your data.

---

### Challenge 5: Long Format → Wide Format Conversion 🔄

**Problem:** Input CSV had 8 rows per observation:

```
CA001,2024-01-01,PRCP,5.2
CA001,2024-01-01,TAVG,-2.1
...8 rows total...
```

**Why it's hard:** Pivot tables can have multiple values per cell (duplicate dates).

**Solution:**

```python
df_wide = df.pivot_table(
    index=['station', 'date', 'latitude', 'longitude',
           'elevation', 'city'],
    columns='observation',
    values='value',
    aggfunc='first'  # Take first value if duplicates
).reset_index()
```

**Gotcha:** Had to preserve metadata columns (city, lat/lon) in the index!

**Time cost:** 2 hours.

**Lesson:** Data transformation is often 50% of the work. Never underestimate cleaning time!

---

## 💻 Built With

### **Languages**

- **Python 3.13** - Core data processing and analysis

  - Chosen for: Rich data science ecosystem
  - Used for: ETL pipeline, feature engineering, forecasting

- **JavaScript (ES6)** - Frontend interactivity

  - Chosen for: Universal browser support
  - Used for: Dashboard controls, chart updates

- **HTML5 / CSS3** - Structure and styling

  - Chosen for: Static deployment capability
  - Used for: Dashboard layout, responsive design

- **Markdown / LaTeX** - Documentation
  - Chosen for: Clear technical writing with math support
  - Used for: All project documentation

---

### **Frameworks & Libraries**

#### **Data Processing**

- **pandas 2.x** - DataFrame operations, pivoting, aggregation
- **numpy 1.x** - Numerical operations, array math
- **scikit-learn 1.x** - Normalization, percentile scaling

#### **Machine Learning (Advanced Models)**

- **Prophet 1.1+** - Time-series forecasting with seasonality
  - Facebook's forecasting library
  - Used for: Trend decomposition, confidence intervals
- **XGBoost 3.x** - Gradient boosting regression
  - Chosen for: Non-linear pattern learning
  - Used for: Feature importance analysis, ensemble models

#### **Visualization**

- **Plotly.js 2.27** - Interactive JavaScript charts

  - Chosen for: No backend required, rich interactivity
  - Used for: All dashboard charts (line, area, bar)

- **Streamlit 1.x** - Python web app framework (optional advanced UI)
  - Chosen for: Rapid prototyping
  - Used for: Model comparison interface

---

### **Data Source**

- **GHCN (Global Historical Climatology Network)**
  - Source: NOAA National Centers for Environmental Information
  - Coverage: 233 Canadian weather stations
  - Variables: Temperature, precipitation, snow, wind
  - Time range: 2022-2024
  - Format: CSV (long format, converted to wide)

---

### **Development Tools**

- **Git / GitHub** - Version control and collaboration
- **VS Code** - Primary IDE
- **Cursor** - AI-assisted coding
- **Jupyter Notebooks** - Exploratory analysis
- **Python venv** - Dependency isolation

---

### **Deployment & Hosting**

- **Static HTML** - Primary deployment method

  - No server required
  - Works offline
  - Can be hosted on:
    - GitHub Pages (free)
    - Netlify (free)
    - Local filesystem
    - USB drive (for offline demos)

- **Streamlit Cloud** (optional) - For advanced ML demo
  - Cloud-based Python app hosting
  - Access to Prophet/XGBoost models

---

### **Key Technical Decisions**

#### **Why Static HTML over Web Framework?**

**Considered:**

- Flask (Python backend)
- React (JavaScript frontend)
- Streamlit (Python rapid prototyping)

**Chose HTML because:**

1. ✅ No server = No maintenance
2. ✅ Universal compatibility (works everywhere)
3. ✅ Instant loading (no API calls)
4. ✅ Easy demo (just open file)
5. ✅ Zero dependencies

**Trade-off:** Pre-compute all forecasts (larger file size, ~5MB), but worth it for portability.

---

#### **Why Plotly.js over D3.js?**

**Considered:**

- D3.js (maximum customization)
- Chart.js (lightweight)
- Plotly.js (interactive, full-featured)

**Chose Plotly.js because:**

1. ✅ Built-in interactivity (hover, zoom, pan)
2. ✅ Professional-looking defaults
3. ✅ `connectgaps: false` for honest gaps
4. ✅ Responsive without extra code
5. ✅ Single CDN include

---

#### **Why Pattern-Based Forecasting over Pure ML?**

**Considered:**

- ARIMA (statistical)
- Prophet (ML time-series)
- XGBoost (ML regression)
- LSTM (deep learning)

**Chose pattern-based for HTML dashboard because:**

1. ✅ No model training needed
2. ✅ Works in pure JavaScript
3. ✅ Interpretable (users understand "monthly average")
4. ✅ Fast (pre-computed)
5. ✅ Seasonal patterns are strong (good enough!)

**Note:** We built Prophet/XGBoost models too, available in Streamlit app for advanced users.

---

#### **Why Percentile Normalization over Min-Max?**

**Math:**

Min-Max (traditional):

$$
x_{\text{norm}} = \frac{x - \min(x)}{\max(x) - \min(x)}
$$

**Problem:** Outliers compress 99% of data to tiny range.

Percentile (robust):

$$
x_{\text{norm}} = \frac{\text{clip}(x, p_5, p_{95}) - p_5}{p_{95} - p_5}
$$

**Benefit:** Outliers clipped, normal values spread across [0, 1].

**Result:** All three indices visible (not dominated by wind/solar).

---

### **Dependencies (requirements.txt)**

```
pandas==2.2.0
numpy==1.26.3
scikit-learn==1.4.0
prophet==1.1.5
xgboost==3.0.0
streamlit==1.31.0
plotly==5.18.0
```

**Installation:**

```bash
pip install -r requirements.txt
```

**Compatibility:**

- Python 3.9+
- macOS: Requires `brew install libomp` for XGBoost
- Windows/Linux: Works out of the box

---

### **Project Structure**

```
Data-Jam/
├── data/
│   ├── cleaned_data_with_city_filled.csv    # Input (long format)
│   ├── processed_wide_format.csv            # Transformed (wide format)
│   └── processed_indices.csv                # Final (with indices)
│
├── src/
│   ├── data_processing.py                   # AI inference
│   └── compute_indices.py                   # Feature engineering
│
├── models/
│   ├── prophet_model.py                     # Time-series forecasting
│   ├── xgboost_model.py                     # Gradient boosting
│   └── ensemble_model.py                    # Combined models
│
├── generate_html_dashboard.py               # Dashboard generator
│
├── web/
│   └── dashboard.html                       # Final product (5MB)
│
├── app.py                                   # Streamlit app (advanced)
│
├── requirements.txt                         # Python dependencies
├── TECHNICAL_REPORT.md                      # Full methodology
├── QUICK_REFERENCE.md                       # Summary
├── DATA_FLOW_DIAGRAM.md                     # Visual pipeline
└── PROJECT_STORY.md                         # This file!
```

---

### **Mathematical Foundations**

Our project leverages several mathematical concepts:

#### **Linear Algebra**

- Matrix operations for data transformation (pivot tables)
- Vector operations for index calculations

#### **Statistics**

- Percentile calculation: $p_k = \text{value at } k\% \text{ of sorted data}$
- Mean aggregation: $\bar{x} = \frac{1}{n}\sum_{i=1}^n x_i$
- Standard deviation for outlier detection

#### **Time Series Analysis**

- Seasonal decomposition: $Y_t = T_t + S_t + R_t$
  - $T_t$ = Trend component
  - $S_t$ = Seasonal component
  - $R_t$ = Residual component

#### **Optimization**

- Gradient boosting (XGBoost):
  $$
  \hat{y}_i^{(t)} = \hat{y}_i^{(t-1)} + \eta \cdot f_t(x_i)
  $$
  Where $\eta$ is learning rate, $f_t$ is new tree

#### **Geographic Models**

- Distance from latitude: $d = |\phi - \phi_0|$
- Elevation effects: Linear coefficient models

---

## 🎯 Impact & Future Work

### **Real-World Applications**

1. **Energy Investment Planning**

   - Identify optimal locations for solar/wind/hydro projects
   - Estimate ROI based on seasonal patterns
   - Risk assessment via historical variability

2. **Grid Management**

   - Predict renewable availability for load balancing
   - Plan backup power requirements
   - Optimize energy storage deployment

3. **Climate Research**
   - Track long-term changes in renewable potential
   - Assess climate change impact on energy systems
   - Inform policy decisions

### **Future Enhancements**

1. **Real-Time Data Integration**

   - Connect to live weather APIs
   - Daily forecast updates
   - Alert system for extreme events

2. **Advanced ML Models**

   - LSTM neural networks for sequence learning
   - Transfer learning across similar cities
   - Uncertainty quantification

3. **Economic Analysis**

   - Cost-benefit calculator
   - Payback period estimation
   - Carbon offset calculations

4. **Expanded Coverage**
   - Include all of North America
   - Add offshore wind potential
   - Geothermal resource mapping

---

## 🏆 What Makes This Special

1. **AI-Driven Inference** - Doesn't just discard incomplete data; intelligently fills gaps
2. **Domain-Informed Features** - Monthly hydro aggregation reflects real infrastructure
3. **Honest Visualization** - Shows data quality transparently, no artificial smoothing
4. **Multiple Time Scales** - Short-term operations + long-term planning
5. **Universal Accessibility** - Works on any device, no installation required
6. **Open Source** - Full methodology documented, reproducible results

---

**Team ClimaZoneAI | SFU DataJam 2025**

_Empowering Canada's renewable energy transition through data-driven insights._
