# NH SOS Multi-Term Scraper

A robust web scraper for the New Hampshire Secretary of State Business Inquiry system that searches for businesses using multiple search terms, filters for active businesses, and deduplicates against existing data.

## Overview

This scraper automates the process of searching for businesses on the NH SOS QuickStart portal, then processes the results to identify new prospects not already in your database.

## Features

- **Multi-term search**: Automatically searches using 15 different business-related terms
- **State persistence**: Saves progress after each session, allowing you to stop and resume
- **Smart filtering**: Only processes businesses with "Good Standing" or "Active" status
- **Automatic deduplication**: Compares against HubSpot and target files using exact and fuzzy matching
- **Minimal output**: Creates only 3 CSV files: progress.csv, matched.csv, and final_data.csv

## Requirements

- Python 3.7+
- Playwright
- Pandas
- RapidFuzz
- AsyncIO support

## Installation

1. Clone this repository
2. Install required packages:
   ```bash
   pip install playwright pandas asyncio rapidfuzz
   playwright install chromium
   ```
3. Create the CSV directory:
   ```bash
   mkdir csvs
   ```

## Project Structure

```
├── main.py               # Entry point with integrated processing
├── scraper.py            # Main scraping logic
├── browser.py            # Browser automation
├── state.py              # State persistence
├── config.py             # Configuration settings
├── nh_scraper_state.json # State file (auto-generated)
└── csvs/                 # CSV directory
    ├── progress.csv      # Scraping progress (all data)
    ├── matched.csv       # Businesses that exist in your database
    ├── final_data.csv    # New prospects (ready to use)
    ├── hubspot.csv       # Your HubSpot data (you provide)
    └── targets_*.csv     # Your existing business data (you provide)
```

## Setup

1. Place your existing data files in the `csvs/` directory:
   - `hubspot.csv` - Must have an "Associated Company" column
   - `targets_*.csv` - Any number of target files, must have a "business_name" column

2. Run the scraper:
   ```bash
   python main.py
   ```

## How It Works

1. **Scraping Phase**: 
   - Searches each term on NH SOS website
   - Extracts business information
   - Saves all data to `progress.csv`
   - Can be stopped and resumed at any time

2. **Processing Phase** (runs automatically when scraping completes):
   - Filters for active businesses only
   - Cleans and standardizes the data
   - Compares against your existing data (HubSpot + targets)
   - Uses both exact and fuzzy matching (95% threshold)
   - Creates final output files

## Output Files

Only 3 CSV files are created in the `csvs/` directory:

### progress.csv
- Used during scraping to track progress
- Contains all scraped data
- Automatically maintained by the scraper

### matched.csv
- Businesses that already exist in your database
- Two columns: business_name, matched_name
- Shows what each business matched to

### final_data.csv
- **This is your main output file**
- Contains new prospects not in your existing data
- Includes: business_name, previous_name, address, agent, status
- Ready for import into your CRM

## Configuration

Edit `config.py` to modify:

- **Search terms**: List of terms to search for
- **Timing settings**: Min/max wait times (15-25 seconds default)
- **Fuzzy match threshold**: Default 95% similarity

## Usage Examples

### Normal Run
```bash
python main.py
```

### Resuming After Interruption
Just run again - it automatically resumes:
```bash
python main.py
```

### Checking Progress
The scraper shows progress for each search term and estimates completion.

## Best Practices

1. **Prepare your data**: Ensure HubSpot and target files are in the correct format
2. **Run during off-peak hours** to minimize server impact
3. **Let it complete**: The deduplication only runs after all scraping is done
4. **Monitor progress**: Watch the terminal for status updates

## Troubleshooting

**No comparison data found**: Make sure your HubSpot and target files are in the `csvs/` directory with the correct column names.

**Browser check detected**: The site has anti-bot measures. Increase wait times in `config.py` if this happens frequently.

**Fuzzy matching takes too long**: You can increase the threshold in `config.py` to be more strict (e.g., 98 instead of 95).

## Notes

- The scraper runs in non-headless mode so you can see what's happening
- All businesses are processed, but only active ones make it to the final output
- Fuzzy matching catches variations like "ABC Trucking LLC" vs "ABC Trucking"
- Progress is saved incrementally, making the process very resilient