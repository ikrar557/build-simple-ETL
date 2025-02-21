from utils.extract.scraper import scrape_main
from utils.transform.transform import transform_data
from utils.load.csv_loader import save_to_csv
from utils.load.db_loader import save_to_postgresql
from utils.load.sheets_loader import save_to_sheets
from datetime import datetime

def main():
    try:
        # Extract
        print("Starting data extraction...")
        raw_data = scrape_main()
        print(f"Extracted {len(raw_data)} items\n")

        # Transform
        print("Starting data transformation...")
        transformed_data = transform_data(raw_data)
        print(f"Transformed {len(transformed_data)} items\n")

        # Load
        print("Starting data loading...")
        
        # Save to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"products_{timestamp}.csv"
        if save_to_csv(transformed_data, csv_filename):
            print(f"✓ Successfully saved data to CSV: {csv_filename}")

        # Save to Google Sheets
        spreadsheet_id = "1oe1pTN0O4qUwPstWVUyStOyRzGgmbF4aRdOVtxfrkXA"
        if save_to_sheets(transformed_data, spreadsheet_id):
            print("✓ Successfully saved data to Google Sheets")
        
        # Save to PostgreSQL
        if save_to_postgresql(transformed_data):
            print("✓ Successfully saved data to PostgreSQL")
        
        print("\nETL process completed successfully!")
        
    except Exception as e:
        print(f"Error in ETL process: {str(e)}")
        raise

if __name__ == "__main__":
    main()