# 🌤️ ClimaZoneAI – Predicting Canada’s Renewable Energy Potential

## 🗣️ Pitch Summary
> “ClimaZoneAI focuses on Canada’s renewable future.  
> We take weather data, apply scientific formulas, and forecast solar, wind, and hydro energy potential for every city.  
> With monthly, seasonal, and annual predictions, we give industries and policymakers a clear view of when and where renewable power will be strongest — for smarter, cleaner energy use.”

## 🔍 Overview
ClimaZoneAI is an AI-powered forecasting platform that predicts **renewable energy potential** for Canadian cities.  
We use historical weather data to estimate how much solar, wind, and hydro energy could be generated in a region.  
By combining weather patterns, elevation, and precipitation data, ClimaZoneAI helps industries and city planners make **smarter, data-driven energy decisions**.

---

## ⚠️ Problem Statement
Canadian industries often operate on fixed electricity schedules, paying high grid costs even when renewable energy is abundant.  
At the same time, Canada’s large renewable potential—especially from wind and hydro—is underused because **weather-based availability** isn’t forecasted well.  

Our question:
> How can we predict the potential of renewable energy for each city, using real weather data, to optimize energy use and reduce costs?

---

## 💡 Our Approach
We simplified our dataset to focus **only on Canada**, using region-specific records from the Global Historical Climatology Network (GHCN).  
From this, ClimaZoneAI:
1. Extracts and cleans key weather variables (temperature, wind speed, snow depth, and precipitation).  
2. Uses **custom formulas and elevation-based assumptions** to estimate renewable energy indices:
   - **Solar Index** – based on temperature and cloud/precipitation patterns  
   - **Wind Index** – derived from average and peak wind speeds  
   - **Hydro Index** – estimated from snow, rain, and elevation data  
3. Computes short-term and long-term indices for:
   - **30-day (Monthly)** potential  
   - **Quarterly (Seasonal)** potential  
   - **Yearly** potential  
4. Trains forecasting models to predict future renewable potential for each index type.

---

## 📊 Methodology Workflow

| Step | Description | Tools |
|------|--------------|-------|
| 1 | Clean & preprocess Canadian weather data | Pandas, NumPy |
| 2 | Apply formulas using elevation, wind, and precipitation | Python logic |
| 3 | Compute Solar, Wind, Hydro indices | Custom functions |
| 4 | Plot graphs for monthly, quarterly, and yearly trends | Matplotlib, Plotly |
| 5 | Train algorithms for prediction using historical data | Scikit-Learn / Prophet |

---

## 🧠 Example
**City Input:** Vancouver  
**Computed Indices (Example Year):**  
- Solar Index (avg): 0.72  
- Wind Index (avg): 0.69  
- Hydro Index (avg): 0.82  

**Predicted Trends:**  
- 30-day graph → short-term fluctuations  
- Quarterly graph → seasonal variations  
- Yearly graph → average renewable potential trend  

---

## 📈 Outputs
1. **Graphs**
   - 30-day, quarterly, and annual renewable energy potential for each city  
2. **Indices**
   - Computed scores for Solar, Wind, and Hydro (0–1 scale)  
3. **Forecasts**
   - Predicted next-year renewable potential based on trained patterns  
4. **Insights**
   - Seasonal confidence intervals and climate consistency reports per energy type  

---

## 🌍 Outcomes
- Identify **where** and **when** renewable energy potential is highest in Canada.  
- Help industries align production with clean energy availability.  
- Support **data-driven planning** for investment in local renewable zones.  

---

## 💻 Tech Stack
**Languages:** Python  
**Libraries:** Pandas, NumPy, Matplotlib, Plotly, Prophet  
**Dataset:** Simplified GHCN (Canadian Region Only)  
**Forecast Model:** Time-series regression + seasonal trend estimation  

---

## 🏁 Deliverables
- Interactive plots for monthly, quarterly, and yearly energy trends  
- Predictive models for solar, hydro, and wind index forecasting  
- Simple dashboard for city-based renewable predictions  
- Presentation-ready graphs and insights  


