from utils.extract import scrape_main
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_sheets, save_to_postgresql

def main():
    try:
        raw_data = scrape_main()
        print(f"Extracted {len(raw_data)} items")
        
        clean_data = transform_data(raw_data)
        print(f"Transformed {len(clean_data)} items")
        
        # Save to CSV
        save_to_csv(clean_data)
        
        # Save to Google Sheets
        SPREADSHEET_ID = '1oe1pTN0O4qUwPstWVUyStOyRzGgmbF4aRdOVtxfrkXA'
        save_to_sheets(clean_data, SPREADSHEET_ID)
        
        # Save to PostgreSQL
        save_to_postgresql(clean_data, {})
        
    except Exception as e:
        print(f"Error in ETL pipeline: {str(e)}")

if __name__ == "__main__":
    main()