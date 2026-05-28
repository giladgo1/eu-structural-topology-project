"""Plotting helpers for EDA notebooks."""

from pathlib import Path
import matplotlib.pyplot as plt


def save_current_figure(path: str | Path, dpi: int = 300) -> None:
    """Save current matplotlib figure with tight layout."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=dpi, bbox_inches="tight")
