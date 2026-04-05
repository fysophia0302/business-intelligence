"""
main.py
=======
Automates weekly retail report extraction from a web reporting portal.

Navigates the portal using Playwright, extracts OSAT and key metrics
for two brand groups across four time periods (last week, last 4 weeks,
last 12 weeks, YTD), and exports the results to Excel.

Usage:
    python main.py
"""

import logging

from playwright.sync_api import sync_playwright

from config import (
    SUPERMARKET_BRANDS, DISCOUNT_BRANDS,
    DATE_RANGE_LAST_WEEK, DATE_RANGE_LAST_4_WEEKS,
    DATE_RANGE_LAST_12_WEEKS, DATE_RANGE_CUSTOM,
    get_ytd_end_date,
)
from scraper import launch_report, run_report_with_retry
from exporter import create_pivot, export_to_excel

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
log = logging.getLogger(__name__)


def main():
    ytd_end = get_ytd_end_date()
    log.info(f"starting extraction — YTD end date: {ytd_end}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page    = browser.new_page()
        frame   = launch_report(page)

        log.info("=== extracting Supermarket data ===")
        sm_last_wk   = run_report_with_retry(frame, SUPERMARKET_BRANDS, DATE_RANGE_LAST_WEEK)
        sm_last_4wk  = run_report_with_retry(frame, SUPERMARKET_BRANDS, DATE_RANGE_LAST_4_WEEKS)
        sm_last_12wk = run_report_with_retry(frame, SUPERMARKET_BRANDS, DATE_RANGE_LAST_12_WEEKS)
        sm_ytd       = run_report_with_retry(frame, SUPERMARKET_BRANDS, DATE_RANGE_CUSTOM, ytd_end)
        log.info("Supermarket extraction complete")

        log.info("=== extracting Discount data ===")
        dc_last_wk   = run_report_with_retry(frame, DISCOUNT_BRANDS, DATE_RANGE_LAST_WEEK)
        dc_last_4wk  = run_report_with_retry(frame, DISCOUNT_BRANDS, DATE_RANGE_LAST_4_WEEKS)
        dc_last_12wk = run_report_with_retry(frame, DISCOUNT_BRANDS, DATE_RANGE_LAST_12_WEEKS)
        dc_ytd       = run_report_with_retry(frame, DISCOUNT_BRANDS, DATE_RANGE_CUSTOM, ytd_end)
        log.info("Discount extraction complete")

        browser.close()

    log.info("building pivot tables and exporting...")
    sm_pivot = create_pivot(sm_last_wk, sm_last_4wk, sm_last_12wk, sm_ytd)
    dc_pivot = create_pivot(dc_last_wk, dc_last_4wk, dc_last_12wk, dc_ytd)
    output   = export_to_excel(sm_pivot, dc_pivot)

    log.info(f"done — file saved to {output}")


if __name__ == "__main__":
    main()
