from utils.extract import scrape_main
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_sheets, save_to_postgresql

def main():
    try:
        # Extract
        raw_data = scrape_main()
        print(f"Extracted {len(raw_data)} items")
        
        # Transform
        clean_data = transform_data(raw_data)
        print(f"Transformed {len(clean_data)} items")
        
        # Load
        save_to_csv(clean_data)
        
    except Exception as e:
        print(f"Error in ETL pipeline: {str(e)}")

if __name__ == "__main__":
    main()