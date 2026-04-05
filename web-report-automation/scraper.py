"""
scraper.py
==========
Playwright automation to navigate the reporting portal,
apply filters, and extract summary table data.

Note: the portal has a known rendering bug where filter selections
need to be applied twice to get correct results — this is handled
in run_report_with_retry().
"""

import time
from io import StringIO

import pandas as pd
from playwright.sync_api import Page, Frame

from config import (
    REPORT_URL, REPORT_NAME, REPORT_SECTION,
    DATE_RANGE_LAST_WEEK, DATE_RANGE_LAST_4_WEEKS,
    DATE_RANGE_LAST_12_WEEKS, DATE_RANGE_CUSTOM,
    DATE_RANGE_MAP, YTD_START_DATE, get_ytd_end_date, METRICS
)


def launch_report(page: Page) -> Frame:
    """Navigate to the reporting portal and return the report iframe frame."""
    page.goto(REPORT_URL)
    page.wait_for_selector("#appLauncherIcon", timeout=0)
    page.click("#appLauncherIcon")
    page.click(f"div.tile-text-wrapper:has-text('{REPORT_SECTION}')")
    page.click(f"text={REPORT_SECTION}")
    page.wait_for_selector(f"text={REPORT_NAME}", timeout=60000)
    page.click(f"text= {REPORT_NAME}")

    iframe_element = page.query_selector("iframe[src*='/report/app']")
    if not iframe_element:
        raise Exception("report iframe not found")

    frame = iframe_element.content_frame()
    if not frame:
        raise Exception("could not access iframe content")

    return frame


def fetch_table_data(frame: Frame) -> pd.DataFrame | None:
    """
    Wait for the report table to load and extract the Totals row.
    Returns a DataFrame with the metrics columns, or None on failure.
    """
    try:
        frame.wait_for_selector("div#selection-list", state="hidden", timeout=180000)

        frame.wait_for_function(
            """() => {
                const table = document.querySelector('table#textAnalyticsGrid');
                return table && table.querySelectorAll('tbody tr').length > 0;
            }""",
            timeout=30000
        )

        table_html  = frame.inner_html("table#textAnalyticsGrid")
        table_html  = '<table>' + table_html + '</table>'
        df          = pd.read_html(StringIO(table_html))[0]
        totals_row  = df[df['Unnamed: 2'] == 'Totals'][METRICS]

        return totals_row

    except Exception as e:
        print(f"table extraction failed: {e}")
        return None


def apply_date_range(frame: Frame, date_range: str, ytd_end: str | None = None):
    """Select a date range from the dropdown, or fill custom date fields for YTD."""
    frame.wait_for_selector("#quickDateRangeSelect", timeout=60000)

    if date_range == DATE_RANGE_CUSTOM:
        frame.select_option("#quickDateRangeSelect", value="-1")
        frame.wait_for_selector("#calendarListRangeBeginTrigger", state="visible", timeout=60000)
        time.sleep(2)
        frame.fill("#calendarListRangeBeginTrigger", YTD_START_DATE)
        time.sleep(2)
        frame.wait_for_selector("#calendarListRangeEndTrigger", state="visible", timeout=60000)
        frame.fill("#calendarListRangeEndTrigger", ytd_end or get_ytd_end_date())
        frame.click("body")
    else:
        value_map = {
            DATE_RANGE_LAST_WEEK:     "51687",
            DATE_RANGE_LAST_4_WEEKS:  "51700",
            DATE_RANGE_LAST_12_WEEKS: "51702",
        }
        frame.select_option("#quickDateRangeSelect", value=value_map[date_range])

    print(f"date range set: {DATE_RANGE_MAP.get(date_range, date_range)}")


def apply_brand_filter(frame: Frame, brands: list[str]):
    """Select brands from the multi-level brand hierarchy filter."""
    frame.wait_for_selector("#dummySelector", timeout=60000)
    frame.click("#dummySelector")
    frame.click("div.ng-binding.ng-scope:has-text('Brand Hierarchy')")
    frame.locator("div#dummySelector", has_text="Single-Level").click()
    frame.locator("div.ng-binding.ng-scope", has_text="Multi-Level").click()
    frame.click("i.tree-branch-head")

    for brand in brands:
        frame.locator("div.tree-label", has_text=brand).click()

    print(f"brands selected: {brands}")


def run_report(frame: Frame):
    """Click Apply and Run Report."""
    frame.click("button.primary.ng-binding:has-text('Apply')")
    frame.click("div#runButton[alt='Run Report']")


def run_report_with_retry(frame: Frame, brands: list[str], date_range: str, ytd_end: str | None = None) -> pd.DataFrame | None:
    """
    Apply filters and run the report.
    Due to a known portal rendering bug, filters are applied twice
    to ensure the correct data is returned.
    """
    # first pass — triggers the portal to register the selection
    apply_date_range(frame, date_range, ytd_end)
    apply_brand_filter(frame, brands)
    run_report(frame)
    print("first pass submitted — waiting for portal to settle...")

    try:
        frame.wait_for_selector("div#selection-list", state="hidden", timeout=180000)
        frame.wait_for_function(
            """() => {
                const table = document.querySelector('table#textAnalyticsGrid');
                return table && table.querySelectorAll('tbody tr').length > 0;
            }""",
            timeout=30000
        )
    except Exception as e:
        print(f"first pass wait failed (expected for bug workaround): {e}")

    # second pass — gets the actual correct data
    apply_date_range(frame, date_range, ytd_end)
    apply_brand_filter(frame, brands)
    run_report(frame)
    time.sleep(30)
    print("second pass submitted — fetching data...")

    return fetch_table_data(frame)
