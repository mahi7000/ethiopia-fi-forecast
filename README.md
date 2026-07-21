# Forecasting Financial Inclusion in Ethiopia

An end-to-end analytics and forecasting system that tracks and predicts Ethiopia's digital financial transformation across two core dimensions of financial inclusion: **Access** (Account Ownership Rate) and **Usage** (Digital Payment Adoption Rate).

---

## Project Overview

Ethiopia is experiencing rapid digital financial growth driven by platforms like Telebirr, M-Pesa, EthSwitch, and Fayda Digital ID. This project synthesizes sparse historical Global Findex demand-side survey data, supply-side operator metrics, and market event impact models to:
- Enrich national financial inclusion datasets with external indicators and macro drivers.
- Analyze growth patterns, market slowdowns, and demographic gaps (e.g., gender, urban/rural).
- Model structural impacts of policies, product launches, and infrastructure investments.
- Deliver scenario-based forecasts for **2025–2027**.
- Provide an interactive dashboard for stakeholder exploration and decision-making.

---

## Repository Structure

```text
ethiopia-fi-forecast/
├── .github/workflows/      # CI/CD workflows
│   └── unittests.yml
├── data/
│   ├── raw/                # Starter unified dataset & reference codes
│   │   ├── ethiopia_fi_unified_data.csv
│   │   └── reference_codes.csv
│   └── processed/          # Enriched & cleaned datasets
├── notebooks/              # Exploratory and modeling Jupyter notebooks
│   └── README.md
├── src/                    # Python source code modules
│   └── __init__.py
├── dashboard/              # Interactive dashboard application
│   └── app.py
├── tests/                  # Unit and integration tests
│   └── __init__.py
├── models/                 # Serialized model artifacts and output parameters
├── reports/                # Generated figures and analysis reports
│   └── figures/
├── requirements.txt        # Python package dependencies
├── README.md               # Project documentation
└── .gitignore              # Git ignore rules