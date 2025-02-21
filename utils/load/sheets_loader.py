from google.oauth2 import service_account
from googleapiclient.discovery import build

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
        
        return True
        
    except Exception as e:
        raise Exception(f"Error saving to Google Sheets: {str(e)}")