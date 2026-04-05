"""
exporter.py
===========
Transforms extracted report data into pivot tables
and exports them to a formatted Excel file.
"""

import os

import pandas as pd

from config import METRICS, EXPORT_DIR, EXPORT_FILENAME


def create_pivot(last_wk: pd.DataFrame, last_4wk: pd.DataFrame,
                 last_12wk: pd.DataFrame, ytd: pd.DataFrame) -> pd.DataFrame:
    """
    Combine four time-period DataFrames into a single pivot table
    with metrics as rows and date ranges as columns.
    """
    last_wk['Date Range']   = 'Last Week'
    last_4wk['Date Range']  = 'Last 4 Weeks'
    last_12wk['Date Range'] = 'Last 12 Weeks'
    ytd['Date Range']       = 'Year to Date'

    all_data = pd.concat([last_wk, last_4wk, last_12wk, ytd], ignore_index=True)

    pivot_df = (
        all_data
        .melt(
            id_vars='Date Range',
            value_vars=METRICS,
            var_name='Metric',
            value_name='Value'
        )
        .pivot(index='Metric', columns='Date Range', values='Value')
    )

    # keep columns and rows in a consistent order
    pivot_df = pivot_df[['Last Week', 'Last 4 Weeks', 'Last 12 Weeks', 'Year to Date']]
    pivot_df = pivot_df.reindex(METRICS)

    return pivot_df


def export_to_excel(supermarket_pivot: pd.DataFrame, discount_pivot: pd.DataFrame):
    """Write both brand group pivot tables to separate sheets in one Excel file."""
    os.makedirs(EXPORT_DIR, exist_ok=True)
    output_path = os.path.join(EXPORT_DIR, EXPORT_FILENAME)

    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        for sheet_name, df in [("Supermarket", supermarket_pivot), ("Discount", discount_pivot)]:
            df.to_excel(writer, sheet_name=sheet_name)

            # auto-fit column widths
            worksheet = writer.sheets[sheet_name]
            for i, col in enumerate(df.columns):
                col_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i + 1, i + 1, col_width)

    print(f"exported to {output_path}")
    return output_path
