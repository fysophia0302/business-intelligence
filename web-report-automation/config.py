"""
config.py
=========
All configuration for the web report automation pipeline.
Sensitive values (URLs, paths) are generalized for portfolio use.
"""

import os
from datetime import datetime, timedelta

# ============================================================
# Report Portal Config
# ============================================================
REPORT_URL      = os.environ.get("REPORT_URL", "https://your-reporting-portal.com/program/your-program-id/home")
REPORT_NAME     = "Retail Summary Report v2"
REPORT_SECTION  = "RETAIL IN-STORE - CORE REPORTS"

# ============================================================
# Brand Groups
# ============================================================
SUPERMARKET_BRANDS = ['Brand A', 'Brand B', 'Brand C']
DISCOUNT_BRANDS    = ['Brand D']

# ============================================================
# Date Range Options (portal-specific dropdown values)
# ============================================================
DATE_RANGE_LAST_WEEK    = "LAST_WEEK"
DATE_RANGE_LAST_4_WEEKS = "LAST_4_WEEKS"
DATE_RANGE_LAST_12_WEEKS = "LAST_12_WEEKS"
DATE_RANGE_CUSTOM       = "CUSTOM"

DATE_RANGE_MAP = {
    DATE_RANGE_LAST_WEEK:     "Last Week",
    DATE_RANGE_LAST_4_WEEKS:  "Last 4 Weeks",
    DATE_RANGE_LAST_12_WEEKS: "Last 12 Weeks",
    DATE_RANGE_CUSTOM:        "Year to Date",
}

# ============================================================
# YTD Date Range
# ============================================================
YTD_START_DATE = "01/04/26"   # fiscal year start

def get_ytd_end_date() -> str:
    """Returns last Saturday as the YTD end date."""
    today = datetime.today()
    days_since_saturday = (today.weekday() - 5) % 7
    last_saturday = today - timedelta(days=days_since_saturday)
    return last_saturday.strftime("%m/%d/%y")

# ============================================================
# Metrics to Extract
# ============================================================
METRICS = [
    'In-Store OSAT',
    'Good value for money (Top Box %)',
    'Items In Stock (Top Box %)',
]

# ============================================================
# Export Config
# ============================================================
BASE_EXPORT_DIR = os.environ.get("EXPORT_DIR", r"output/weekly_report")
TODAY_STR       = datetime.today().strftime('%Y-%m-%d')
EXPORT_DIR      = os.path.join(BASE_EXPORT_DIR, TODAY_STR)
EXPORT_FILENAME = f"OSAT_export_{TODAY_STR}.xlsx"
