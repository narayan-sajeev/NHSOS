# processing/processor.py
"""Main data processing pipeline"""

import time

import pandas as pd

import config
from cleaner import clean_business_data
from deduplicator import deduplicate_businesses


def process_scraped_data(df):
    """
    Process scraped data through all steps:
    1. Filter active businesses
    2. Clean data
    3. Deduplicate against existing data (exact match only)
    4. Save results
    """
    print("\n" + "=" * 60)
    print("PROCESSING FINAL DATA")
    print("=" * 60)

    start_time = time.time()

    # Step 1: Filter active businesses only
    print(f"\nStep 1: Filtering active businesses...")
    print(f"Total businesses: {len(df)}")
    active_df = df[df['status'].isin(config.ACTIVE_STATUSES)].copy()
    print(f"Active businesses: {len(active_df)} ({len(active_df) / len(df) * 100:.1f}%)")

    if active_df.empty:
        print("No active businesses found!")
        return

    # Step 2: Clean the data
    print(f"\nStep 2: Cleaning data...")
    active_df = clean_business_data(active_df)

    # Step 3: Deduplicate using exact matching only
    print(f"\nStep 3: Deduplicating against existing data (exact match only)...")
    new_df, matched_df, match_details = deduplicate_businesses(active_df)

    # Step 4: Save results
    print("\nStep 4: Saving results...")

    # Save only display columns for final data
    if not new_df.empty:
        new_df[config.DISPLAY_COLUMNS].to_csv(config.FINAL_DATA_FILE, index=False)
        print(f"✓ Saved {len(new_df)} new prospects to {config.FINAL_DATA_FILE}")
    else:
        print("No new prospects found")
        # Create empty file with headers
        pd.DataFrame(columns=config.DISPLAY_COLUMNS).to_csv(config.FINAL_DATA_FILE, index=False)

    if not matched_df.empty:
        matched_df.to_csv(config.MATCHED_FILE, index=False)
        print(f"✓ Saved {len(matched_df)} matched businesses to {config.MATCHED_FILE}")
    else:
        print("No matches found")
        # Create empty file with headers
        pd.DataFrame(columns=['business_name', 'matched_name']).to_csv(config.MATCHED_FILE, index=False)

    # Print summary
    elapsed_time = time.time() - start_time
    _print_processing_summary(df, active_df, new_df, matched_df, match_details, elapsed_time)


def _print_processing_summary(total_df, active_df, new_df, matched_df, match_details, elapsed_time):
    """Print detailed processing summary."""
    print("\n" + "=" * 60)
    print("PROCESSING SUMMARY")
    print("=" * 60)
    print(f"Total businesses scraped: {len(total_df)}")
    print(f"Active businesses: {len(active_df)} ({len(active_df) / len(total_df) * 100:.1f}%)")
    print(f"New prospects: {len(new_df)} ({len(new_df) / len(active_df) * 100:.1f}% of active)")
    print(f"Exact matches found: {len(matched_df)} ({len(matched_df) / len(active_df) * 100:.1f}% of active)")

    if match_details:
        # Count sources
        source_counts = {}
        for match_info in match_details.values():
            source = match_info.get('source', 'unknown')
            # Simplify source names
            if source.startswith('target_'):
                source = 'target_files'
            source_counts[source] = source_counts.get(source, 0) + 1

        print("\nMatch sources:")
        for source, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {source}: {count}")

    print(f"\nTotal processing time: {elapsed_time:.1f} seconds")
