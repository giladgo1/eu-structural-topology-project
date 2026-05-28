# Investing in Europe's Future

## EU Structural Transition & Policy Priorities

A comparative data analytics capstone project exploring how European countries balance economic growth, sustainability, innovation, resilience, and social welfare priorities over time.

Core logic:

```text
Public Investment Priorities -> Structural Indicators -> Structural Outcomes -> Comparative Insights
```

## Project scope

- Geography: EU27 countries
- Years: 2014–2025
- Sources: Eurostat, OECD optional
- Main dataset: country-year panel
- Approach: exploratory, comparative, non-causal

## Repository structure

```text
data/raw/eurostat/          Raw Eurostat TSV files
data/interim/cleaned_kpis/  Cleaned individual KPI tables
data/processed/             Final master datasets for EDA/Tableau
notebooks/                  Working notebooks
src/                        Reusable Python helpers
reports/figures/            Exported EDA figures
reports/dashboard_mockups/  Dashboard concept images
tableau/exported_data/      Tableau-ready exports
```

## Main datasets produced

- `data/processed/eu_master_filled.csv`
- `data/processed/government_spending_wide.csv`
- `data/processed/eu_master_plus.csv`

## Dashboard concept

### Dashboard 1 — EU Structural Tradeoff Explorer
Exploring structural trends, tradeoffs, and policy patterns across Europe.

### Dashboard 2 — Interactive Strategy Explorer
Explore how different policy priorities align with structural outcomes.

## Setup

```bash
pip install -r requirements.txt
```

Place raw Eurostat files in:

```text
data/raw/eurostat/
```

Then run:

```text
notebooks/01_data_loading_cleaning.py
notebooks/02_preliminary_eda.py
```

These `.py` files are Jupyter-compatible percent-format notebooks and can be opened in VS Code as notebooks.

## Methodological note

This project identifies structural associations and comparative patterns. It does not claim causality, produce forecasts, or prescribe optimal policy.
