from pathlib import Path

# Project root = parent folder of src/
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw" / "eurostat"
INTERIM_DIR = DATA_DIR / "interim"
CLEANED_KPI_DIR = INTERIM_DIR / "cleaned_kpis"
PROCESSED_DIR = DATA_DIR / "processed"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"

# Create output folders if missing
for path in [RAW_DIR, CLEANED_KPI_DIR, PROCESSED_DIR, FIGURES_DIR]:
    path.mkdir(parents=True, exist_ok=True)
