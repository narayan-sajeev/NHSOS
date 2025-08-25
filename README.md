# NH SOS Business Scraper & Processor

## 📌 Overview

This project automates the scraping, cleaning, deduplication, and visualization of **New Hampshire Secretary of State (NH SOS) business records**. It is designed to identify and track trucking-related businesses across New England by searching for industry-specific terms (e.g., *truck, freight, towing, excavation*), cleaning and standardizing records, and storing results in CSV and SQLite databases.

The pipeline integrates **Playwright** for browser automation, **pandas** for data processing, and **Datasette** for interactive exploration.

---

## ⚙️ Features

* **Automated Web Scraping**
  Uses Playwright to query NH SOS with multiple trucking-related search terms.
* **State Persistence**
  Saves progress and resumes scraping if interrupted (`nh_scraper_state.json`).
* **Data Cleaning**
  Standardizes names, addresses, and agent information.
* **Deduplication**
  Removes duplicates by exact-match checking against:

  * Existing HubSpot company records (`hubspot.csv`)
  * Previous scraping outputs (`targets_*.csv`)
* **CSV & Database Outputs**

  * `progress.csv`: Tracks scraped businesses across search terms.
  * `matched.csv`: Businesses matched against existing datasets.
  * `final_data.csv`: Cleaned, deduplicated dataset of active businesses.
* **Visualization**
  Converts final data into an SQLite database and serves it with **Datasette**.

---

## 🗂 Project Structure

```
.
├── main.py             # Entry point: orchestrates scraping + processing
├── scraper.py          # Core scraping logic
├── browser.py          # Browser automation with Playwright
├── state.py            # State persistence (progress across terms/pages)
├── processor.py        # Cleans, filters, deduplicates scraped data
├── cleaner.py          # Utility functions for cleaning names, addresses, agents
├── deduplicator.py     # Deduplicates against HubSpot + target datasets
├── visuals.py          # SQLite + Datasette visualization
├── config.py           # Central configuration (files, search terms, settings)
├── csvs/               # Data storage (progress.csv, matched.csv, final_data.csv, targets_*.csv)
└── nh_scraper_state.json # State file tracking completed pages
```

---

## 🔍 Workflow

1. **Run the scraper**

   ```bash
   python main.py
   ```

   * Iterates through search terms defined in `config.py`.
   * Scrapes businesses from NH SOS with Playwright.
   * Saves intermediate results in `progress.csv`.

2. **Process scraped data** (`processor.py`)

   * Filters only **active businesses** (`Good Standing`, `Active`).
   * Cleans business names, addresses, and agent details.
   * Deduplicates against HubSpot and existing `targets_*.csv`.

3. **Generate outputs**

   * `progress.csv` → All scraped records with status tracking.
   * `matched.csv` → Records matched to existing datasets.
   * `final_data.csv` → Final cleaned, deduplicated dataset.

4. **Visualize data**

   ```bash
   python visuals.py
   ```

   * Loads `final_data.csv` into SQLite (`nh_sos_data.db`).
   * Launches Datasette for querying and visualization.

---

## 📊 Example Data Flow

1. Scraping term **“truck”** → Collects 175 pages of businesses.
2. State stored in `nh_scraper_state.json` so it can resume if stopped.
3. Deduplication removes overlaps with `hubspot.csv` and previous `targets_*.csv`.
4. Cleaned results written into `final_data.csv` for further use.

---

## 🛠 Requirements

* **Python 3.9+**
* Dependencies:

  ```bash
  pip install pandas playwright sqlite-utils datasette
  ```
* Playwright setup:

  ```bash
  playwright install
  ```

---

## 🚀 Usage

* **Start a new scrape**:

  ```bash
  python main.py
  ```
* **Resume after interruption**:
  State will auto-load from `nh_scraper_state.json`.
* **Process and clean existing data**:

  ```bash
  python processor.py
  ```
* **Explore results in browser**:

  ```bash
  python visuals.py
  ```

---

## 📂 Key Outputs

* `progress.csv` → Raw scrape progress.
* `matched.csv` → Businesses matched against existing datasets.
* `final_data.csv` → Cleaned, deduplicated, active businesses (main deliverable).
* `nh_sos_data.db` → SQLite database for visualization.

---

## 🔮 Future Improvements

* Add **fuzzy deduplication** (beyond exact matches).
* Expand beyond NH SOS to other state registries.
* Build **Power BI / dashboard integration** for executives.