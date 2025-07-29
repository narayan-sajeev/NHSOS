"""
Clean NH SOS CSV data and create a new CSV with only display columns
"""
import pandas as pd
from data_cleaner import clean_business_data

# Configuration
INPUT_CSV = "nh_active_only.csv"
OUTPUT_CSV = "nh_cleaned_data.csv"

# Columns to keep (as shown in Datasette)
DISPLAY_COLUMNS = ['business_name', 'previous_name', 'address', 'agent', 'status']


def main():
    """Load, clean, and save CSV with only display columns."""
    
    # Load the original CSV
    print(f"Loading {INPUT_CSV}...")
    df = pd.read_csv(INPUT_CSV)
    print(f"Loaded {len(df)} rows")
    
    # Clean the data
    print("Cleaning data...")
    df = clean_business_data(df)
    
    # Keep only display columns
    df_display = df[DISPLAY_COLUMNS]
    
    # Save to new CSV
    print(f"Saving cleaned data to {OUTPUT_CSV}...")
    df_display.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved {len(df_display)} rows with {len(DISPLAY_COLUMNS)} columns")
    
    # Show sample of cleaned data
    print("\nSample of cleaned data:")
    print(df_display.head(10))
    
    # Show column info
    print(f"\nColumns in output file: {', '.join(DISPLAY_COLUMNS)}")


if __name__ == "__main__":
    main()
