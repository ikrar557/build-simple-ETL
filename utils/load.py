import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import psycopg2

def save_to_csv(data, filename='products.csv'):
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        return True
    except Exception as e:
        raise Exception(f"Error saving to CSV: {str(e)}")

def save_to_sheets(data, spreadsheet_id):
    try:
        # Google Sheets authentication and saving logic
        pass
    except Exception as e:
        raise Exception(f"Error saving to Google Sheets: {str(e)}")

def save_to_postgresql(data, connection_params):
    try:
        # PostgreSQL connection and saving logic
        pass
    except Exception as e:
        raise Exception(f"Error saving to PostgreSQL: {str(e)}")