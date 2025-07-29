"""
NH SOS Data Visualization with Datasette
"""
import sqlite3
import subprocess

import pandas as pd

from data_cleaner import clean_business_data

# Configuration
CSV_FILE = "nh_active_only.csv"
DB_FILE = "nh_sos_data.db"


def create_database():
    """Create SQLite database with cleaned data."""
    # Load and clean data
    df = pd.read_csv(CSV_FILE)
    df = clean_business_data(df)

    # Create database
    with sqlite3.connect(DB_FILE) as conn:
        # Main table without unwanted columns
        display_columns = ['business_name', 'previous_name', 'address',
                           'agent', 'status']
        df[display_columns].to_sql('truck_sales', conn, if_exists='replace', index=False)

        # Create indexes for performance
        conn.execute("CREATE INDEX idx_status ON truck_sales(status)")
        conn.execute("CREATE INDEX idx_name ON truck_sales(business_name)")


def launch():
    """Launch Datasette."""
    create_database()

    subprocess.run([
        "datasette", DB_FILE,
        "--open"
    ])


if __name__ == "__main__":
    launch()
