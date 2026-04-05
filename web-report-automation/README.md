# Web Report Automation

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Playwright](https://img.shields.io/badge/Playwright-Automation-orange)
![Pandas](https://img.shields.io/badge/Pandas-Excel%20Export-green)
![Status](https://img.shields.io/badge/Status-Production-brightgreen)

Automates weekly retail report extraction from a web-based reporting portal.
Navigates the portal using Playwright, extracts OSAT and key retail metrics
for multiple brand groups across four time periods, and exports the results
to a formatted Excel file.

## Architecture

```
Reporting Portal (Web) → Playwright Automation → Data Extraction → Pivot Table → Excel Export
```

## Project Structure

```
web-report-automation/
├── main.py          # entry point — orchestrates the full workflow
├── config.py        # all configuration: brands, date ranges, export paths
├── scraper.py       # Playwright navigation and data extraction
├── exporter.py      # pivot table creation and Excel export
└── requirements.txt
```

## Features

- Automated browser navigation using Playwright
- Extracts metrics across 4 time periods: Last Week, Last 4 Weeks, Last 12 Weeks, YTD
- Handles a known portal rendering bug via a retry pattern
- Auto-calculates YTD end date (last Saturday)
- Exports clean pivot tables to Excel with auto-fitted column widths

## Metrics Extracted

- In-Store OSAT
- Good value for money (Top Box %)
- Items In Stock (Top Box %)

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
playwright install chromium
```

Set environment variables:

```bash
export REPORT_URL=your-reporting-portal-url
export EXPORT_DIR=your-export-directory
```

Run:

```bash
python main.py
```

## Output

An Excel file with two sheets — one per brand group — each containing
a pivot table of metrics by time period.

## Note

Portal URL, brand names, and internal dropdown values are generalized.
This script is designed for a proprietary reporting portal and requires
valid credentials and network access to run.
```
