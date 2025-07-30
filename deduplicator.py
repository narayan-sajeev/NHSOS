# processing/deduplicator.py
"""Business deduplication using exact matching only"""

import os
import glob
import pandas as pd

import config
from cleaner import normalize_for_matching


def load_comparison_data():
    """Load HubSpot and target files for comparison."""
    existing_names = []
    sources = []
    
    # Load HubSpot data
    hubspot_path = os.path.join(config.CSV_DIR, "hubspot.csv")
    if os.path.exists(hubspot_path):
        try:
            hubspot_df = pd.read_csv(hubspot_path)
            company_names = hubspot_df['Associated Company'].dropna().tolist()
            existing_names.extend(company_names)
            sources.extend(['hubspot'] * len(company_names))
            print(f"Loaded {len(company_names)} companies from HubSpot")
        except Exception as e:
            print(f"Could not load HubSpot data: {e}")
    
    # Load all target files (targets_*.csv)
    target_pattern = os.path.join(config.CSV_DIR, "targets_*.csv")
    target_files = glob.glob(target_pattern)
    
    for target_file in target_files:
        try:
            target_df = pd.read_csv(target_file)
            names = target_df['business_name'].dropna().tolist()
            existing_names.extend(names)
            sources.extend([f'target_{os.path.basename(target_file)}'] * len(names))
            print(f"Loaded {len(names)} businesses from {os.path.basename(target_file)}")
        except Exception as e:
            print(f"Could not load {target_file}: {e}")
    
    print(f"\nTotal existing businesses to check against: {len(existing_names)}")
    return existing_names, sources


def create_normalized_lookup(names, sources):
    """
    Create a dictionary mapping normalized names to original names and sources.
    If multiple entries have the same normalized name, keep track of all.
    """
    lookup = {}
    for name, source in zip(names, sources):
        norm_name = normalize_for_matching(name)
        if norm_name:  # Skip empty normalized names
            if norm_name not in lookup:
                lookup[norm_name] = []
            lookup[norm_name].append({
                'original': name,
                'source': source
            })
    return lookup


def deduplicate_businesses(df):
    """
    Deduplicate businesses using exact matching only (case-insensitive).
    Returns: new_prospects_df, matched_existing_df, match_details
    """
    # Load comparison data
    existing_names, sources = load_comparison_data()
    
    if not existing_names:
        print("Warning: No comparison data found. All businesses will be considered new.")
        return df, pd.DataFrame(), {}
    
    # Create normalized lookup dictionary
    print("\nCreating lookup dictionary for exact matching...")
    lookup_dict = create_normalized_lookup(existing_names, sources)
    
    # Normalize scraped business names
    df['normalized'] = df['business_name'].apply(normalize_for_matching)
    
    # Perform exact matching
    print("Performing exact matches (case-insensitive)...")
    matches = {}
    matched_rows = []
    new_rows = []
    
    for idx, row in df.iterrows():
        norm_name = row['normalized']
        
        if norm_name and norm_name in lookup_dict:
            # Found exact match
            match_info = lookup_dict[norm_name][0]  # Take first match if multiple
            matches[idx] = {
                'matched_name': match_info['original'],
                'source': match_info['source'],
                'match_type': 'exact'
            }
            matched_rows.append({
                'business_name': row['business_name'],
                'matched_name': match_info['original']
            })
        else:
            # No match found
            new_rows.append(row.to_dict())
    
    # Create dataframes
    new_df = pd.DataFrame(new_rows)
    matched_df = pd.DataFrame(matched_rows)
    
    # Remove normalized column from new dataframe
    if 'normalized' in new_df.columns:
        new_df = new_df.drop('normalized', axis=1)
    
    # Remove normalized column from original dataframe
    if 'normalized' in df.columns:
        df.drop('normalized', axis=1, inplace=True)
    
    print(f"Found {len(matched_df)} exact matches")
    print(f"Found {len(new_df)} new prospects")
    
    return new_df, matched_df, matches