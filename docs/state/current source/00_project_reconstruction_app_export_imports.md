# 0. Project Reconstruction / App Export Imports

This file documents the standard reconstruction workflow for restarting notebooks or continuing the project in a fresh chat/session.

## Purpose

After a kernel restart, temporary notebook objects disappear.

Examples of objects that may disappear:

- `country_structural_summary_v2_dimensions`
- `pathway_dimension_signatures`
- `cluster_plot_df`
- `static_vs_dynamic`
- `family_df`
- `kmeans_results`

To avoid repeated `NameError` issues, each notebook should begin with a reconstruction section that reloads the stable app exports from `data/app/`.

## Standard notebook reconstruction cell

Use this at the top of future notebooks:

    import sys
    from pathlib import Path

    PROJECT_ROOT = Path(
        r"C:\Users\gilad\Documents\Data Analytics course 02_26\capstone-eu-structural-tradeoffs"
    )

    sys.path.append(str(PROJECT_ROOT / "src"))

    from project_reconstruction import (
        load_app_exports,
        verify_app_exports,
        assign_common_tables_to_globals
    )

    tables = load_app_exports(PROJECT_ROOT)
    verify_app_exports(tables)
    assign_common_tables_to_globals(tables, globals())

## Required app exports

These files should exist in `data/app/`:

- `country_structural_summary_v2_dimensions.csv`
- `country_dimension_profiles.csv`
- `tradeoff_space_coordinates.csv`
- `pathway_dimension_signatures.csv`
- `structural_family_metadata.csv`
- `tradeoff_space_classification.csv`

Optional if created:

- `relative_adaptation_shift.csv`
- `investment_response_shifts.csv`

## Workflow rule

Before running downstream plotting, clustering, app, or dashboard cells:

1. Run the reconstruction cell.
2. Verify table shapes.
3. Confirm required columns exist.
4. Then continue analysis.

This should become the first section of future notebooks.
