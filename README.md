# NH SOS Multi-Term Scraper

A robust web scraper for the New Hampshire Secretary of State Business Inquiry system that searches for businesses using multiple search terms and handles pagination, rate limiting, and session management.

## Overview

This scraper automates the process of searching for businesses on the NH SOS QuickStart portal using predefined search terms. It's designed to be resilient, with features like state persistence, automatic retry logic, and intelligent rate limiting to avoid detection.

## Features

- **Multi-term search**: Automatically searches using 15 different business-related terms
- **State persistence**: Saves progress after each session, allowing you to stop and resume at any time
- **Smart pagination**: Handles large result sets with intelligent page navigation
- **Rate limiting**: Random delays between sessions (15-25 seconds) to avoid detection
- **Batch processing**: Processes 6 pages per batch, max 11 pages per session
- **Error recovery**: Tracks failed pages and handles browser checks gracefully
- **Duplicate detection**: Automatically removes duplicate businesses by ID
- **Export options**: Generates both complete dataset and active-only business lists

## Requirements

- Python 3.7+
- Playwright
- Pandas
- AsyncIO support

## Installation

1. Clone this repository
2. Install required packages:
   ```bash
   pip install playwright pandas asyncio
   playwright install chromium
   ```

## Project Structure

```
├── main.py           # Entry point - orchestrates the scraping process
├── scraper.py        # Main scraping logic and session management
├── browser.py        # Browser automation and page interactions
├── state.py          # State persistence and management
├── config.py         # Configuration settings
├── nh_scraper_state.json    # State file (auto-generated)
├── nh_progress_all.csv      # Progress file with all businesses
├── nh_final_data.csv        # Final cleaned dataset
└── nh_active_only.csv       # Active businesses only
```

## Configuration

Edit `config.py` to modify:

- **Search terms**: List of terms to search for
- **Timing settings**: Min/max wait times, pages per batch
- **File paths**: Output file locations
- **Browser settings**: User agent, viewport size

Default search terms:
- truck, freight, transport, excavation, trailer
- ltl, haul, grading, sitework, aggregates
- paving, asphalt, concrete, diesel, towing

## Usage

Simply run the main script:

```bash
python main.py
```

The scraper will:
1. Load any previous state (if resuming)
2. Search each term sequentially
3. Navigate through all pages of results
4. Extract business information
5. Save progress after each batch
6. Generate final CSV files when complete

### Stopping and Resuming

- Press `Ctrl+C` to stop gracefully at any time
- Progress is automatically saved
- Run `python main.py` again to resume from where you left off

## Output Files

### nh_progress_all.csv
Contains all scraped businesses with columns:
- `business_name`: Company name
- `business_id`: Unique NH business ID
- `homestate_name`: Home state name
- `previous_name`: Previous business names
- `business_type`: Entity type (LLC, Corp, etc.)
- `address`: Business address
- `agent`: Registered agent
- `status`: Current status
- `search_term`: Which search term found this business

### nh_active_only.csv
Filtered subset containing only businesses with status "Good Standing" or "Active"

### nh_scraper_state.json
Tracks scraping progress including:
- Completed pages by search term
- Failed pages for retry
- Total pages detected per term
- Current search term being processed

## Error Handling

The scraper handles several error scenarios:
- **Browser checks**: Detects and reports when hitting anti-bot measures
- **Page navigation failures**: Attempts direct page jumps for efficiency
- **Network timeouts**: 30-second timeout for page loads
- **Invalid pages**: Detects when reaching beyond available pages

## Performance

- Processes approximately 6-11 pages per session
- 15-25 second delays between sessions
- Average runtime depends on total pages
- Typical page processing: 2-3 seconds per page

## Best Practices

1. **Run during off-peak hours** to minimize impact on the server
2. **Monitor the browser window** - it runs in non-headless mode for debugging
3. **Check state file** if you need to manually adjust progress
4. **Keep delays reasonable** - faster isn't always better for stability

## Troubleshooting

**Browser check detected**: The site has anti-automation measures. Current settings usually avoid this, but if it happens frequently, increase wait times in `config.py`

**Navigation failures**: Some pages may fail to load. The scraper tracks these and you can manually check failed pages in the state file

**Duplicate businesses**: Automatically handled - the scraper deduplicates by `business_id`

## License

This tool is for educational and research purposes. Ensure you comply with the website's terms of service and `robots.txt`.

## Notes

- The scraper uses Playwright with Chromium in non-headless mode
- Each search term is completed before moving to the next
- Progress is saved incrementally, making it very resilient to interruptions
- The "Page X of Y" detection helps optimize navigation for large result sets