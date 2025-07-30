# processing/cleaner.py
"""Data cleaning utilities for business data"""

import re
import pandas as pd


def clean_business_name(name):
    """Clean and format business names."""
    if pd.isna(name) or not name:
        return ''
    
    name = str(name).strip()
    
    # Fix spacing issues
    name = re.sub(r'\s+', ' ', name)
    name = re.sub(r'\s*,\s*', ', ', name)
    
    # Simple title case
    name = name.title()
    
    return name


def clean_address(address):
    """Clean and standardize addresses."""
    if pd.isna(address) or not address:
        return ''
    
    address = str(address).strip()
    
    # Fix spacing issues
    address = re.sub(r'\s+', ' ', address)
    address = re.sub(r'\s*,\s*', ', ', address)
    
    # Simple title case
    address = address.title()
    
    # Remove trailing USA if present
    address = re.sub(r',?\s*Usa\s*', '', address)
    
    return address.strip()


def clean_agent_name(name):
    """Clean agent names."""
    if pd.isna(name) or not name:
        return ''
    
    name = str(name).strip()
    
    # Fix spacing
    name = re.sub(r'\s+', ' ', name)
    
    # Simple title case
    name = name.title()
    
    # Handle "Last, First" format
    if ',' in name and name.count(',') == 1:
        parts = name.split(',')
        if len(parts) == 2:
            last, first = parts[0].strip(), parts[1].strip()
            name = f"{first} {last}"
    
    return name


def clean_business_data(df):
    """Clean all business data fields."""
    df = df.copy()
    
    # Clean business names
    df['business_name'] = df['business_name'].apply(clean_business_name)
    
    # Clean previous names
    df['previous_name'] = df['previous_name'].fillna('').apply(clean_business_name)
    
    # Clean addresses
    df['address'] = df['address'].apply(clean_address)
    
    # Clean agent names
    df['agent'] = df['agent'].fillna('').apply(clean_agent_name)
    
    # Standardize status
    df['status'] = df['status'].fillna('Unknown')
    
    return df


def normalize_for_matching(name):
    """
    Normalize business names for exact matching (case-insensitive).
    This is used for comparison only, not for display.
    """
    if pd.isna(name) or not name:
        return ''
    
    name = str(name).lower().strip()
    
    # Remove common business suffixes
    suffix_pattern = r'\s*,?\s*(llc|inc|corp|corporation|company|co|ltd|limited|lp|llp|pc|pllc)\.?\s*$'
    name = re.sub(suffix_pattern, '', name, flags=re.IGNORECASE)
    
    # Remove special characters but keep spaces
    name = re.sub(r'[^\w\s]', ' ', name)
    
    # Normalize whitespace
    name = ' '.join(name.split())
    
    return name