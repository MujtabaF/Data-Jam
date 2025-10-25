# ClimaZoneAI - Complete Technology Stack

## 📋 Complete List of Technologies Used

---

## 🔤 Programming Languages

1. **Python 3.13**
   - Core data processing and analysis
   - Machine learning model implementation
   - Dashboard generation scripts

2. **JavaScript (ES6)**
   - Client-side interactivity
   - Chart rendering and updates
   - DOM manipulation

3. **HTML5**
   - Semantic markup
   - Dashboard structure
   - Form controls

4. **CSS3**
   - Responsive styling
   - Animations and transitions
   - Grid and flexbox layouts

5. **SQL** (via pandas)
   - Data querying operations
   - Aggregation logic

6. **Markdown**
   - Documentation
   - Reports and guides

7. **LaTeX**
   - Mathematical formulas in documentation
   - Scientific notation

8. **Bash/Shell**
   - Automation scripts
   - Installation commands

---

## 📚 Python Libraries & Frameworks

### Core Data Processing
1. **pandas 2.2.0**
   - DataFrame operations
   - CSV reading/writing
   - Pivot tables
   - Groupby aggregations
   - Time series handling

2. **numpy 1.26.3**
   - Numerical computations
   - Array operations
   - Mathematical functions
   - Statistical operations

3. **scikit-learn 1.4.0**
   - MinMaxScaler (normalization)
   - Preprocessing utilities
   - Model evaluation metrics

### Machine Learning & Forecasting
4. **Prophet 1.1.5**
   - Time-series forecasting
   - Seasonal decomposition
   - Trend analysis
   - Confidence intervals
   - Holiday effects

5. **XGBoost 3.0.0**
   - Gradient boosting
   - Regression models
   - Feature importance
   - Cross-validation
   - Hyperparameter tuning

### Web Application Framework
6. **Streamlit 1.31.0**
   - Interactive web apps
   - Real-time updates
   - Widget controls
   - Session state management
   - Caching decorators

### Visualization
7. **Plotly 5.18.0**
   - Python plotting library
   - Figure generation
   - Interactive charts
   - Export utilities

### Utilities
8. **datetime** (built-in)
   - Date manipulation
   - Timedelta calculations
   - Date parsing

9. **json** (built-in)
   - JSON serialization
   - Data export for web

10. **os** (built-in)
    - File system operations
    - Path manipulation
    - Directory creation

11. **sys** (built-in)
    - System-specific parameters
    - Path configuration

---

## 🎨 JavaScript Libraries & Frameworks

1. **Plotly.js 2.27.0**
   - Interactive charts (line, area, bar)
   - Hover tooltips
   - Zoom and pan
   - Responsive layouts
   - Export to PNG/SVG

2. **Vanilla JavaScript (ES6)**
   - No additional frameworks
   - Native DOM API
   - Event listeners
   - Async/await
   - Arrow functions
   - Template literals

---

## 📊 Data Sources & APIs

1. **GHCN (Global Historical Climatology Network)**
   - Provider: NOAA (National Oceanic and Atmospheric Administration)
   - Data: Historical weather observations
   - Coverage: 233 Canadian weather stations
   - Variables: PRCP, TAVG, TMAX, TMIN, SNOW, SNWD, AWND, WSF2
   - Format: CSV (long format)
   - Time Range: 2022-2024
   - Access: Public dataset

2. **NOAA NCEI (National Centers for Environmental Information)**
   - Source of GHCN data
   - Free access, no API key required

---

## 🖥️ Platforms & Operating Systems

1. **macOS 24.1.0**
   - Primary development platform
   - Darwin kernel
   - zsh shell

2. **Cross-Platform Compatibility**
   - Windows (tested)
   - Linux (supported)
   - macOS (primary)

3. **Web Browsers**
   - Chrome/Chromium
   - Firefox
   - Safari
   - Edge
   - Mobile browsers (iOS Safari, Chrome Mobile)

---

## ☁️ Cloud Services & Hosting

1. **GitHub**
   - Version control
   - Repository hosting
   - Collaboration
   - Issue tracking

2. **GitHub Pages** (deployment option)
   - Static site hosting
   - Free tier
   - Custom domains
   - HTTPS support

3. **Netlify** (deployment option)
   - Static site hosting
   - Drag-and-drop deployment
   - Automatic builds
   - CDN distribution

4. **Streamlit Cloud** (optional)
   - Python app hosting
   - Automatic deployment from GitHub
   - Free tier for public apps

---

## 💾 Databases & Storage

1. **CSV Files** (primary storage)
   - `cleaned_data_with_city_filled.csv` (input)
   - `processed_wide_format.csv` (intermediate)
   - `processed_indices.csv` (final)

2. **JSON** (embedded data)
   - Forecast data embedded in HTML
   - City/province mappings
   - Chart configurations

3. **In-Memory Storage**
   - Pandas DataFrames
   - Python dictionaries
   - JavaScript objects

*Note: No traditional database (SQL/NoSQL) used - all data processing done in-memory*

---

## 🛠️ Development Tools

1. **VS Code (Visual Studio Code)**
   - Primary IDE
   - Extensions: Python, Jupyter, Markdown

2. **Cursor**
   - AI-assisted coding
   - Code completion
   - Refactoring assistance

3. **Jupyter Notebook**
   - Exploratory data analysis
   - Prototyping
   - Visualization testing

4. **Git**
   - Version control
   - Branching and merging
   - Commit history

5. **pip (Package Installer for Python)**
   - Dependency management
   - Version pinning
   - Virtual environment support

6. **venv (Python Virtual Environment)**
   - Dependency isolation
   - Project-specific packages

7. **Homebrew** (macOS)
   - Package manager
   - Installing system dependencies (libomp)

8. **Terminal/iTerm2**
   - Command-line interface
   - Script execution

---

## 📦 Build & Deployment Tools

1. **Python Scripts**
   - `generate_html_dashboard.py` - Dashboard generator
   - `src/compute_indices.py` - Index calculation
   - `src/data_processing.py` - Data cleaning

2. **requirements.txt**
   - Python dependency specification
   - Version pinning

3. **GitHub Actions** (potential use)
   - CI/CD pipelines
   - Automated testing

---

## 🎨 UI/UX Technologies

1. **CSS Grid**
   - Layout system
   - Responsive design

2. **Flexbox**
   - Component alignment
   - Flexible layouts

3. **CSS Variables**
   - Theme management
   - Color schemes

4. **Media Queries**
   - Responsive breakpoints
   - Mobile optimization

5. **CSS Gradients**
   - Background styling
   - Visual effects

6. **Box Shadow**
   - Depth and elevation
   - Card effects

7. **Transitions & Animations**
   - Hover effects
   - Smooth state changes

---

## 📈 Visualization & Charting

1. **Plotly.js**
   - Primary charting library
   - Line charts
   - Area charts
   - Bar charts
   - Scatter plots

2. **Plotly Python**
   - Figure generation in Python
   - Export to HTML

3. **Chart Configuration**
   - Custom color schemes
   - Responsive layouts
   - Interactive legends
   - Hover templates

---

## 🧮 Mathematical & Statistical Tools

1. **NumPy Mathematical Functions**
   - np.clip() - Value clamping
   - np.mean() - Averages
   - np.std() - Standard deviation
   - np.percentile() - Percentile calculations

2. **Pandas Statistical Functions**
   - quantile() - Percentile computation
   - describe() - Summary statistics
   - groupby() - Aggregations
   - rolling() - Moving windows

3. **Statistical Methods**
   - Percentile-based normalization
   - Mean aggregation
   - Seasonal decomposition
   - Pattern recognition

---

## 🔧 System Dependencies

1. **libomp (OpenMP)**
   - Parallel processing library
   - Required by XGBoost on macOS
   - Installed via Homebrew

2. **Python Development Headers**
   - C extensions compilation
   - Binary module support

---

## 📝 Documentation Tools

1. **Markdown**
   - README files
   - Technical reports
   - Quick references

2. **LaTeX (via Markdown)**
   - Mathematical notation
   - Formulas and equations

3. **ASCII Art**
   - Data flow diagrams
   - Visual documentation

4. **Code Comments**
   - Inline documentation
   - Docstrings

---

## 🧪 Testing & Quality Assurance

1. **Manual Testing**
   - Cross-browser testing
   - Device testing (desktop, tablet, mobile)
   - Data validation

2. **Data Quality Checks**
   - NaN detection
   - Outlier filtering
   - Range validation

3. **Error Handling**
   - Try-except blocks
   - Graceful degradation
   - User feedback

---

## 🌐 Web Technologies

1. **HTTP/HTTPS**
   - Static file serving
   - Secure connections

2. **CDN (Content Delivery Network)**
   - Plotly.js via CDN
   - Fast global access

3. **File Protocol**
   - Local HTML file access
   - Offline functionality

4. **JSON**
   - Data interchange format
   - Configuration storage

---

## 🔐 Security & Best Practices

1. **Input Validation**
   - Data type checking
   - Range validation

2. **Error Handling**
   - Exception management
   - User-friendly error messages

3. **Code Quality**
   - PEP 8 style guide (Python)
   - ESLint principles (JavaScript)
   - Clean code practices

---

## 📱 Responsive Design Technologies

1. **Viewport Meta Tag**
   - Mobile optimization
   - Scale control

2. **Responsive Units**
   - rem, em (relative sizing)
   - % (percentage-based)
   - vw, vh (viewport-based)

3. **Mobile-First Design**
   - Progressive enhancement
   - Touch-friendly controls

---

## 🚀 Performance Optimization

1. **Data Pre-computation**
   - All forecasts generated ahead of time
   - Embedded in HTML

2. **Efficient Algorithms**
   - O(n log n) sorting
   - Vectorized operations (NumPy)
   - Batch processing

3. **Caching (Streamlit)**
   - @st.cache_data decorator
   - Memoization

---

## 📋 File Formats

1. **CSV (Comma-Separated Values)**
   - Input data
   - Intermediate results
   - Final indices

2. **JSON (JavaScript Object Notation)**
   - Embedded data
   - Configuration files

3. **HTML (HyperText Markup Language)**
   - Dashboard output
   - Documentation

4. **Markdown (.md)**
   - Documentation files
   - Reports

5. **Python Scripts (.py)**
   - Processing pipelines
   - Model implementations

---

## 🎯 Domain-Specific Technologies

1. **Time Series Analysis**
   - Seasonal pattern recognition
   - Trend decomposition
   - Forecasting algorithms

2. **Geographic Information Processing**
   - Latitude/longitude calculations
   - Elevation-based adjustments
   - Distance metrics

3. **Meteorological Domain Knowledge**
   - Weather variable relationships
   - Climate patterns
   - Physical heuristics

---

## 🔄 Data Processing Technologies

1. **ETL (Extract, Transform, Load)**
   - Data extraction from CSV
   - Long-to-wide format transformation
   - Index calculation and loading

2. **Data Cleaning**
   - Missing value imputation
   - Outlier detection
   - Data validation

3. **Feature Engineering**
   - Derived features
   - Temporal features
   - Geographic features

---

## 📊 Business Intelligence Tools

1. **Metrics Dashboards**
   - KPI cards
   - Summary statistics
   - Visual indicators

2. **Interactive Filters**
   - Dropdown selectors
   - Dynamic updates
   - User-driven exploration

---

## Summary by Category

### **Languages: 8**
Python, JavaScript, HTML, CSS, SQL, Markdown, LaTeX, Bash

### **Python Libraries: 11**
pandas, numpy, scikit-learn, Prophet, XGBoost, Streamlit, Plotly, datetime, json, os, sys

### **JavaScript Libraries: 2**
Plotly.js, Vanilla JavaScript (ES6)

### **Data Sources: 2**
GHCN, NOAA NCEI

### **Platforms: 3**
macOS, Windows (compatible), Linux (compatible)

### **Cloud Services: 4**
GitHub, GitHub Pages, Netlify, Streamlit Cloud

### **Databases: 3**
CSV files, JSON, In-memory (no traditional DB)

### **Development Tools: 8**
VS Code, Cursor, Jupyter, Git, pip, venv, Homebrew, Terminal

### **Visualization Tools: 2**
Plotly.js, Plotly Python

### **File Formats: 5**
CSV, JSON, HTML, Markdown, Python

---

## 🏆 Total Technologies: 50+

This project leverages **over 50 different technologies, tools, and frameworks** spanning:
- Data science
- Machine learning
- Web development
- Cloud deployment
- Geographic information systems
- Time series analysis
- Interactive visualization
- Documentation
- Version control
- Development tooling

All orchestrated to create a comprehensive renewable energy forecasting platform! 🌍⚡

---

**Team ClimaZoneAI | SFU DataJam 2025**

