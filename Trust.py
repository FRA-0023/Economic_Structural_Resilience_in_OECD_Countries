#!/usr/bin/env python3
from pathlib import Path
import asyncio
import pandas as pd
import io
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

# -----------------------
# CONFIG
# -----------------------
AGENCY_ID = "OECD.GOV.GIP"
DATAFLOW_ID = "DSD_GOV_TRUST@DF_GOV_TRUST"
VERSION = "latest"               # or "all"
BASE_URL = "https://sdmx.oecd.org/public/rest/data"
TARGET_URL = f"{BASE_URL}/{AGENCY_ID},{DATAFLOW_ID},{VERSION}/all"
PARAMS = "dimensionAtObservation=AllDimensions&format=csvfilewithlabels"
REQUEST_URL = f"{TARGET_URL}?{PARAMS}"

PROJECT_ROOT = Path.cwd()
DATA_RAW_DIR = PROJECT_ROOT / "Data" / "Raw"
DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = "OECD_Trust_Institutions_2000_2025.csv"
OUTPUT_PATH = DATA_RAW_DIR / OUTPUT_FILE

# -----------------------
# Fetch + save using Playwright
# -----------------------
async def fetch_and_save(url: str, output_path: Path, timeout_ms: int = 120_000):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            locale="en-US"
        )
        page = await context.new_page()
        try:
            print("Navigating to endpoint (Playwright will run page JS/challenge)...")
            response = await page.goto(url, timeout=timeout_ms)
            await page.wait_for_load_state("networkidle", timeout=timeout_ms)

            if response is None:
                raise RuntimeError("No response received from server.")

            status = response.status
            print("HTTP status:", status)
            if status != 200:
                body = await response.text()
                raise RuntimeError(f"HTTP {status} when fetching data. Preview:\n{body[:2000]}")

            text = await response.text()

            # If response body doesn't look like CSV, attempt an in-page fetch
            if not text.strip().startswith(("REF_AREA", "Country", "TIME_PERIOD")):
                fetched = await page.evaluate(
                    f"""() => fetch("{url}", {{headers: {{'Accept': 'application/vnd.sdmx.data+csv; charset=utf-8'}}}})
                                .then(r => r.text())
                                .catch(err => "PLAYWRIGHT_FETCH_ERROR: " + err.toString())"""
                )
                if isinstance(fetched, str) and fetched.startswith("PLAYWRIGHT_FETCH_ERROR"):
                    raise RuntimeError(f"Playwright page fetch failed: {fetched}")
                text = fetched

            df_raw = pd.read_csv(io.StringIO(text), low_memory=False)
            print("Columns detected:", df_raw.columns.tolist())

            # Try indicator filter if present
            if "INDICATOR" in df_raw.columns:
                df_work = df_raw[df_raw["INDICATOR"] == "T1"].copy()
            else:
                df_work = df_raw.copy()

            required = ["REF_AREA", "TIME_PERIOD", "OBS_VALUE"]
            missing = [c for c in required if c not in df_work.columns]
            if missing:
                raise RuntimeError(f"Missing columns needed for tidy output: {missing}")

            df_tidy = (
                df_work[required]
                .rename(columns={"REF_AREA": "Country", "TIME_PERIOD": "Year", "OBS_VALUE": "Value"})
                .sort_values(["Country", "Year"])
                .reset_index(drop=True)
            )

            df_tidy.to_csv(output_path, index=False)
            print(f"Saved {len(df_tidy)} rows to {output_path}")

        except PlaywrightTimeoutError as e:
            raise RuntimeError(f"Playwright timeout: {e}")
        finally:
            await context.close()
            await browser.close()

# -----------------------
# Entrypoint
# -----------------------
def main():
    # Prevent re-downloading if file already exists
    if OUTPUT_PATH.exists():
        print(f"File already exists. Skipping: {OUTPUT_PATH}")
        return

    asyncio.run(fetch_and_save(REQUEST_URL, OUTPUT_PATH))

if __name__ == "__main__":
    main()
