# %% [markdown]
# # 02 Preliminary EDA
# Loads the processed master dataset only. No raw cleaning here.

# %%
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from scipy.stats import zscore

sys.path.append(str(Path.cwd().parent))

from src.config import PROCESSED_DIR, FIGURES_DIR, make_dirs
from src.plotting import save_current_figure

make_dirs()

# %%
eu_master_plus = pd.read_csv(PROCESSED_DIR / "eu_master_plus.csv")
print(eu_master_plus.shape)
display(eu_master_plus.head())

# %% [markdown]
# Add EDA plots here: EU trends, case-country trajectories, spending priorities, heatmaps.
