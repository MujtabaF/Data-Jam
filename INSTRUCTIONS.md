# 🚀 ClimaZoneAI - Getting Started

A simple guide to get your renewable energy forecasting dashboard up and running.

---

## 📋 Prerequisites

- **Python 3.8+** (Check with: `python --version`)
- **pip** (Python package installer)
- Your data file: `data/cleaned_data_with_city_filled.csv`

---

## ⚡ Quick Start (3 Steps)

### Step 1: Install Dependencies

Open your terminal and navigate to the project folder:

```bash
cd /Users/shengzhan/Documents/Github_Repos/Data-Jam
```

Install required packages:

```bash
pip install -r requirements.txt
```

⏱️ This will take 2-5 minutes depending on your internet speed.

---

### Step 2: Run the Pipeline

Execute the main script:

```bash
python run_pipeline.py
```

This will:

1. ✅ Process your data (~30 seconds)
2. ✅ Compute renewable energy indices (~1 minute)
3. ✅ Launch the interactive dashboard (opens in browser automatically)

---

### Step 3: Use the Dashboard

The dashboard will open at: **http://localhost:8501**

If it doesn't open automatically, copy this URL into your browser.

**What you can do:**

- 📍 Select any Canadian province and city
- 📊 View historical Solar/Wind/Hydro trends
- 🔮 Generate forecasts (30 days, 4 months, or 1 year)
- 📈 Compare Prophet, XGBoost, and Ensemble models
- 💾 Download forecast results as CSV

---

## 🎮 Usage Tips

### First Time Running

The first run will process all data. Subsequent runs will be faster.

### Changing Forecast Settings

In the dashboard sidebar, you can:

- Switch provinces/cities
- Change forecast horizon
- Toggle model visibility

### Stopping the Dashboard

Press `Ctrl + C` in your terminal to stop the server.

---

## 🔄 Alternative: Step-by-Step Manual Run

If you prefer to run each step separately:

```bash
# 1. Process data
python src/prepare_data.py

# 2. Compute indices
python src/compute_indices.py

# 3. Launch dashboard
streamlit run app.py
```

---

## 💡 Advanced Options

### Skip Data Processing (if already done)

```bash
python run_pipeline.py --skip-prep
```

### Skip Index Computation (if already done)

```bash
python run_pipeline.py --skip-indices
```

### Launch Dashboard Only (no preprocessing)

```bash
python run_pipeline.py --dashboard-only
```

Or directly:

```bash
streamlit run app.py
```

---

## 🐛 Troubleshooting

### Issue: "Command not found: python"

**Solution:** Try `python3` instead:

```bash
python3 run_pipeline.py
```

---

### Issue: "ModuleNotFoundError: No module named 'prophet'"

**Solution:** Install dependencies:

```bash
pip install -r requirements.txt
```

Or if using Python 3:

```bash
pip3 install -r requirements.txt
```

---

### Issue: "Data file not found"

**Solution:** Make sure your data file exists at:

```
data/cleaned_data_with_city_filled.csv
```

Check with:

```bash
ls data/cleaned_data_with_city_filled.csv
```

---

### Issue: Dashboard won't load / Port already in use

**Solution:** Try a different port:

```bash
streamlit run app.py --server.port 8502
```

Then open: http://localhost:8502

---

### Issue: Prophet installation fails on Mac M1/M2

**Solution:** Install via conda:

```bash
conda install -c conda-forge prophet
```

---

### Issue: Very slow model training

**Solution:** This is normal for the first run. The dashboard uses caching, so:

- First forecast: 10-30 seconds
- Subsequent forecasts: 1-2 seconds

---

## 📊 What to Expect

### First Run Timeline

1. **Data Processing** → 30-60 seconds
2. **Index Computation** → 1-2 minutes
3. **Dashboard Launch** → 5 seconds
4. **First Model Training** → 10-30 seconds (per city)

### After First Run

- Dashboard launches instantly
- Switching cities trains new models (10-20 seconds)
- Changing forecast horizon is instant (uses cached models)

---

## 🎯 Demo Workflow

For a quick demo/presentation:

1. Run: `python run_pipeline.py`
2. Wait for browser to open (or go to http://localhost:8501)
3. Select: **Province = British Columbia**, **City = Vancouver**
4. View **Historical Analysis** tab (impressive charts!)
5. Switch to **Forecast** tab
6. Select **365 days (1 year)** forecast
7. Watch models train (show the progress spinner!)
8. Compare three models (point out confidence intervals)
9. Switch to **Model Insights** tab (show feature importance)
10. Download CSV (show practical value)

**Time:** ~3 minutes total

---

## 📁 Key Files Overview

```
📦 Project Structure
│
├── 🚀 run_pipeline.py          # ⭐ START HERE - One command to run everything
├── 🌐 app.py                   # Main dashboard application
│
├── 📂 data/
│   └── cleaned_data_with_city_filled.csv  # Your input data (required)
│
├── 📂 src/
│   ├── prepare_data.py         # Step 1: Convert data format
│   └── compute_indices.py      # Step 2: Calculate renewable indices
│
└── 📂 models/
    ├── prophet_model.py        # Time-series forecasting
    ├── xgboost_model.py        # Machine learning forecasting
    └── ensemble_model.py       # Combined model (best performance)
```

---

## 🆘 Need Help?

### Check These Documents

1. **QUICKSTART.txt** - Basic usage guide
2. **PROJECT_SUMMARY.md** - Complete feature list
3. **DEMO_SCRIPT.txt** - Hackathon presentation guide

### Common Commands Reference

```bash
# Full pipeline (recommended)
python run_pipeline.py

# Dashboard only (if data already processed)
streamlit run app.py

# Process data manually
python src/prepare_data.py
python src/compute_indices.py

# Check if data file exists
ls -lh data/cleaned_data_with_city_filled.csv

# Check Python version
python --version

# Check installed packages
pip list | grep -E "prophet|xgboost|streamlit"
```

---

## ✅ Success Checklist

Before presenting/demoing:

- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Data file exists at correct location
- [ ] Can run `python run_pipeline.py` without errors
- [ ] Dashboard opens in browser
- [ ] Can select province and city
- [ ] Can generate forecasts
- [ ] Charts display correctly

---

## 🎉 You're Ready!

If the dashboard is running at http://localhost:8501 and showing data, **you're all set!**

Enjoy exploring renewable energy forecasts across Canada! 🇨🇦🌍⚡

---

## 📞 Quick Reference

| What                 | Command                         |
| -------------------- | ------------------------------- |
| **Start Everything** | `python run_pipeline.py`        |
| **Dashboard Only**   | `streamlit run app.py`          |
| **Stop Server**      | `Ctrl + C`                      |
| **View in Browser**  | http://localhost:8501           |
| **Help**             | `python run_pipeline.py --help` |

---

**Last Updated:** 2025-10-25  
**Project:** ClimaZoneAI - SFU DataJam 2025  
**Team:** Team ClimaZoneAI 🌤️
