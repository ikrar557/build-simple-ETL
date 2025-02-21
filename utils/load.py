import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import psycopg2
from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

def save_to_csv(data, filename='products.csv'):
    try:
        if not isinstance(data, list):
            raise TypeError("Input data must be a list")
            
        if not data:
            raise ValueError("No data to save")
            
        if not isinstance(filename, str):
            raise TypeError("Filename must be a string")
            
        if not filename.endswith('.csv'):
            filename = f"{filename}.csv"
            
        df = pd.DataFrame(data)
        required_columns = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'timestamp']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
            
        df.to_csv(filename, index=False)
        print(f"Successfully saved {len(data)} records to {filename}")
        return True
        
    except Exception as e:
        raise Exception(f"Error saving to CSV: {str(e)}")

def save_to_sheets(data, spreadsheet_id):
    try:
        if not isinstance(data, list) or not data:
            raise ValueError("Invalid or empty data")
            
        if not isinstance(spreadsheet_id, str) or not spreadsheet_id:
            raise ValueError("Invalid spreadsheet ID")
        
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = service_account.Credentials.from_service_account_file(
            'google-sheets-api.json',
            scopes=SCOPES
        )
        
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        
        headers = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'timestamp']
        values = [headers] 
        
        for item in data:
            row = [
                item.get('Title', ''),
                item.get('Price', 0),
                item.get('Rating', 0),
                item.get('Colors', 0),
                item.get('Size', ''),
                item.get('Gender', ''),
                item.get('timestamp', '')
            ]
            values.append(row)
        
        body = {
            'values': values
        }
        
        range_name = 'Sheet1!A1:G' + str(len(values))
        
        sheet.values().clear(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        
        result = sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"Successfully updated {result.get('updatedCells')} cells in Google Sheets")
        return True
        
    except Exception as e:
        raise Exception(f"Error saving to Google Sheets: {str(e)}")

def save_to_postgresql(data, connection_params):
    try:
        if not isinstance(data, list) or not data:
            raise ValueError("Invalid or empty data")
            
        # Get credentials from environment variables
        default_params = {
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'port': os.getenv('DB_PORT')
        }
        
        db_url = f"postgresql://{default_params['user']}:{default_params['password']}@{default_params['host']}:{default_params['port']}/{default_params['database']}"
        engine = create_engine(db_url)
        
        Base = declarative_base()
        
        class Product(Base):
            __tablename__ = 'scraped_products'
            
            Title = Column(String, primary_key=True)
            Price = Column(Float)
            Rating = Column(Float)
            Colors = Column(Integer)
            Size = Column(String)
            Gender = Column(String)
            timestamp = Column(String)
        
        Base.metadata.create_all(engine)
        
        Session = sessionmaker(bind=engine)
        session = Session()
        
        try:
            session.query(Product).delete()
            
            for item in data:
                product = Product(
                    Title=item['Title'],
                    Price=item['Price'],
                    Rating=item['Rating'],
                    Colors=item['Colors'],
                    Size=item['Size'],
                    Gender=item['Gender'],
                    timestamp=item['timestamp']
                )
                session.add(product)
            
            session.commit()
            print(f"Successfully saved {len(data)} records to PostgreSQL")
            return True
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            
    except Exception as e:
        raise Exception(f"Error saving to PostgreSQL: {str(e)}")