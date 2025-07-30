# config.py
"""Configuration for NH scraper"""

import os

# CSV directory
CSV_DIR = "csvs"

# File names
STATE_FILE = "nh_scraper_state.json"  # Keep state file in root
PROGRESS_FILE = os.path.join(CSV_DIR, "progress.csv")
MATCHED_FILE = os.path.join(CSV_DIR, "matched.csv")
FINAL_DATA_FILE = os.path.join(CSV_DIR, "final_data.csv")

# Search terms
SEARCH_TERMS = [
    "truck", "freight", "transport", "excavation", "trailer",
    "ltl", "haul", "grading", "sitework", "aggregates",
    "paving", "asphalt", "concrete", "diesel", "towing"
]

# Timing
MIN_WAIT = 15
MAX_WAIT = 25
PAGES_PER_BATCH = 6
MAX_PAGES_PER_SESSION = 11

# Browser
VIEWPORT = {'width': 1920, 'height': 1080}
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
BASE_URL = "https://quickstart.sos.nh.gov/online/BusinessInquire"

# Display columns for final output
DISPLAY_COLUMNS = ['business_name', 'previous_name', 'address', 'agent', 'status']

# Active statuses to filter
ACTIVE_STATUSES = ['Good Standing', 'Active']