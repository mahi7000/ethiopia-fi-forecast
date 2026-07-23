# Ethiopia Financial Inclusion Analysis & Forecasting (2011–2028)

An end-to-end data engineering, statistical impact modeling, and interactive forecasting platform analyzing financial inclusion trajectories, digital payment adoption, and macro-policy interventions in Ethiopia.

---

## Project Overview

This repository provides quantitative frameworks and interactive visualization tools designed for policy research and strategic decision-making in digital financial services. It evaluates progress from historical Global Findex benchmarks (2011–2024), quantifies non-linear policy/market event impacts, forecasts financial access and digital payment usage (2025–2028), and tracks national alignment targets.

### Key Capabilities
- **Schema-Aware Data Ingestion & Wrangling:** Standardized ingestion pipelines handling sparse historical survey observations and granular transactional metrics.
- **Event Impact Modeling:** Mathematical quantification of catalyst events (e.g., Telebirr launch, Fayda Digital ID e-KYC rollout, EthSwitch interoperability) using non-linear temporal logistic ramp-up functions.
- **Scenario Forecasting:** Trend regression models augmented by policy impact vectors under **Baseline**, **Base Policy**, **Optimistic**, and **Pessimistic** macroeconomic scenarios.
- **Interactive Decision Dashboard:** Multi-page Streamlit dashboard equipped with Plotly figures, key metric indicators, scenario simulation tools, and raw data export functionality.

---

## 🛠️ Project Structure

```text
.
├── dashboard/
│   └── app.py                     # Multi-page interactive Streamlit web application
├── data/
│   ├── raw/                       # Historical Global Findex & macroeconomic datasets
│   └── processed/                 # Schema-aligned merged data, matrices, and forecast outputs
├── notebooks/
│   ├── 01_data_wrangling.ipynb    # Data ingestion, schema validation, & preprocessing
│   ├── 02_exploratory_analysis.ipynb # Channel dynamics & P2P vs. ATM crossover analysis
│   ├── 03_event_impact_modeling.ipynb # Temporal ramp-up functions & validation
│   └── 04_forecasting_scenarios.ipynb # Event-augmented trend forecasting (2025–2028)
├── reports/
│   └── figures/                   # Rendered charts, heatmaps, and scenario plots
├── src/
│   ├── data_processing.py         # Pipeline functions for data cleaning and schema validation
│   ├── forecasting.py             # Baseline regression, scenario scaling, & CI calculators
│   └── impact_modeling.py         # Logistic temporal ramp-up & event-indicator matrices
├── tests/
│   ├── test_data_processing.py    # Unit tests for data ingestion routines
│   ├── test_impact_modeling.py    # Unit tests for event matrix & temporal logic
│   └── test_task4.py              # Unit tests for forecasting algorithms
├── .gitignore
├── pytest.ini                     # Pytest configuration settings
├── README.md                      # Project documentation and run instructions
└── requirements.txt               # Dependency specifications

```

---

## Installation & Setup

### Prerequisites

* Python 3.9+
* Git

### Environment Setup

1. **Clone the repository:**
```bash
git clone [https://github.com/your-username/ethiopia-financial-inclusion.git](https://github.com/your-username/ethiopia-financial-inclusion.git)
cd ethiopia-financial-inclusion

```


2. **Create and activate a virtual environment:**
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate

```


3. **Install dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt

```



---

## Running Unit Tests

Verify project pipeline integrity and mathematical models by running `pytest`:

```bash
pytest -v

```

---

## Running the Streamlit Dashboard Locally

Launch the interactive financial inclusion dashboard locally:

1. **Ensure your virtual environment is active.**
2. **Execute the Streamlit application:**
```bash
streamlit run dashboard/app.py

```


3. **Open in browser:** Access `http://localhost:8501`.

### Dashboard Features

* **Overview Page:** Executive metrics summary cards, historical Findex trajectory, and P2P vs. ATM cash withdrawal crossover visualization.
* **Trends Analysis Page:** Interactive time-series explorer with channel filtering (Mobile Money, Bank Accounts, Cards) and CSV download options.
* **Forecasts Page:** 2025–2028 projection curves with $95\%$ confidence interval bands across key target variables.
* **Inclusion Projections & Q&A:** Interactive radial progress gauge assessing progress toward national targets alongside structured answers to strategic consortium queries.

---

## Summary of Main Forecast Results (2025–2028)

### Target: Account Ownership Rate (`ACC_OWNERSHIP`, % of Adults)

| Year | Baseline Trend (%) | Base Policy Scenario (%) | Optimistic Scenario (%) | Pessimistic Scenario (%) | Key Policy Driver |
| --- | --- | --- | --- | --- | --- |
| **2024 (Obs.)** | 49.00% | 49.00% | 49.00% | 49.00% | Global Findex Benchmark |
| **2025** | 50.80% | **53.30%** | **55.10%** | **51.20%** | Fayda Digital ID Integration |
| **2026** | 52.40% | **57.10%** | **60.40%** | **53.80%** | Full Interoperability & Open Banking |
| **2027** | 53.90% | **60.50%** | **65.20%** | **56.10%** | Rural Agent & QR Network Expansion |
| **2028** | 55.30% | **63.40%** | **69.50%** | **58.00%** | Bridge 2030 Horizon Target |

```

[Ethiopia launches second National Digital Payments Strategy](https://www.youtube.com/watch?v=ypCw-9eAOy0)

This video highlights Ethiopia's official launch of its National Digital Payments Strategy, providing valuable context on the key policy drivers and digital transformation goals modeled in this analysis.