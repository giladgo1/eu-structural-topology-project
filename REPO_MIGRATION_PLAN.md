# Migration Plan

## 1. Create the structure
Use the folder structure in this repository.

## 2. Move raw files
Move every downloaded Eurostat TSV into:

```text
data/raw/eurostat/
```

Rename files to short stable names, for example:

```text
gdp_growth.tsv
inflation.tsv
unemployment.tsv
gini.tsv
education.tsv
rnd.tsv
ict_specialists.tsv
renewables.tsv
emissions.tsv
debt.tsv
government_expenditure.tsv
```

## 3. Run cleaning notebook
Run:

```text
notebooks/01_data_loading_cleaning.py
```

This creates:

```text
data/interim/cleaned_kpis/*.csv
data/processed/eu_master_filled.csv
data/processed/government_spending_wide.csv
data/processed/eu_master_plus.csv
```

## 4. Run EDA notebook
Run:

```text
notebooks/02_preliminary_eda.py
```

All EDA must load only:

```text
data/processed/eu_master_plus.csv
```

## 5. Tableau
Connect Tableau to:

```text
data/processed/eu_master_plus.csv
```

Do not connect Tableau to raw TSV files.

## 6. Keep raw and generated data out of Git
The `.gitignore` is configured to avoid committing data files by default.
