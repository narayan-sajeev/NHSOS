# main.py
"""NH SOS Scraper - Main entry point"""

import asyncio
import os
import sys

import pandas as pd

import config
import scraper
from processor import process_scraped_data


def print_header():
    """Print application header."""
    print("\n" + "=" * 80)
    print("NH SOS Multi-Term Scraper v6")
    print(f"Search terms: {', '.join(config.SEARCH_TERMS)}")
    print("Matching: Exact matches only (case-insensitive)")
    print("Output: progress.csv, matched.csv, final_data.csv")
    print("=" * 80 + "\n")


def check_progress_exists():
    """Check if progress.csv exists."""
    return os.path.exists(config.PROGRESS_FILE)


def check_completion_status(state):
    """Check if scraping is complete for all terms."""
    if not state:
        return False

    for term in config.SEARCH_TERMS:
        completed = len(state.completed_pages.get(term, set()))
        total = state.total_pages.get(term)
        if total is None or completed < total:
            return False
    return True


def print_search_term_summary(df):
    """Print summary of businesses by search term."""
    if 'search_term' in df.columns:
        print("\nBusinesses by search term:")
        print(df['search_term'].value_counts())


async def main():
    """Main application entry point."""
    print_header()

    # Check if we should skip scraping and go directly to processing
    if check_progress_exists() and len(sys.argv) > 1 and sys.argv[1] == '--process-only':
        print("Processing mode: Using existing progress.csv")
        df = pd.read_csv(config.PROGRESS_FILE)
        print(f"\nLoaded {len(df)} businesses from progress.csv")
        print_search_term_summary(df)
        process_scraped_data(df)
        return

    state = None
    try:
        # Run the scraper
        state = await scraper.run()
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        print("Progress has been saved - you can resume after fixing the issue")
        return

    # Process results if scraping is complete
    if state:
        scraper.print_final_summary(state)

        if check_completion_status(state) and os.path.exists(config.PROGRESS_FILE):
            # Load scraped data
            df = pd.read_csv(config.PROGRESS_FILE)
            print(f"\nTotal unique businesses scraped: {len(df)}")

            print_search_term_summary(df)

            # Process the data
            process_scraped_data(df)
        else:
            print("\nScraping not complete. Resume to continue collecting data.")
            print("Or run with --process-only flag to process existing data:")
            print("  python main.py --process-only")


if __name__ == "__main__":
    asyncio.run(main())
