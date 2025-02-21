import pytest
from unittest.mock import patch, MagicMock
from utils.load.csv_loader import save_to_csv
from utils.load.db_loader import save_to_postgresql
from utils.load.sheets_loader import save_to_sheets

def test_save_to_csv_with_extension():
    test_data = [{
        'Title': 'Test Product',
        'Price': 160000,
        'Rating': 4.5,
        'Colors': 3,
        'Size': 'M',
        'Gender': 'Unisex',
        'timestamp': '2024-01-01 00:00:00'
    }]
    
    with patch('pandas.DataFrame.to_csv') as mock_to_csv:
        assert save_to_csv(test_data, 'test') == True
        mock_to_csv.assert_called_once()

def test_save_to_postgresql():
    test_data = [{
        'Title': 'Test Product',
        'Price': 160000,
        'Rating': 4.5,
        'Colors': 3,
        'Size': 'M',
        'Gender': 'Unisex',
        'timestamp': '2024-01-01 00:00:00'
    }]
    
    with patch('sqlalchemy.create_engine'), \
         patch('sqlalchemy.orm.sessionmaker'):
        assert save_to_postgresql(test_data) == True

# def test_save_to_postgresql_session_error():
#     test_data = [{
#         'Title': 'Test Product',
#         'Price': 160000,
#         'Rating': 4.5,
#         'Colors': 3,
#         'Size': 'M',
#         'Gender': 'Unisex',
#         'timestamp': '2024-01-01 00:00:00'
#     }]
    
#     # Create mock session with context manager behavior
#     mock_session = MagicMock()
#     mock_session.__enter__.return_value = mock_session
#     mock_session.__exit__.return_value = None
    
#     # Configure session methods
#     mock_session.add.side_effect = Exception("Database error")  # Changed from merge to add
#     mock_session.commit.side_effect = Exception("Database error")
    
#     # Create session factory mock
#     Session = MagicMock()
#     Session.return_value = mock_session
    
#     with patch('sqlalchemy.create_engine'), \
#          patch('sqlalchemy.orm.sessionmaker', return_value=Session), \
#          pytest.raises(Exception) as exc_info:
#         save_to_postgresql(test_data)
    
#     assert "Database error" in str(exc_info.value)

# def test_save_to_sheets():
#     test_data = [{
#         'Title': 'Test Product',
#         'Price': 160000,
#         'Rating': 4.5,
#         'Colors': 3,
#         'Size': 'M',
#         'Gender': 'Unisex',
#         'timestamp': '2024-01-01 00:00:00'
#     }]
    
#     # Set up mock credentials
#     mock_creds = MagicMock()
#     mock_creds.universe_domain = 'googleapis.com'
    
#     # Set up mock service and sheet
#     mock_service = MagicMock()
#     mock_sheet = MagicMock()
#     mock_values = MagicMock()
    
#     # Configure batch_get method to return header data
#     mock_batch_get = MagicMock()
#     mock_batch_get.execute.return_value = {
#         'valueRanges': [
#             {'values': [['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'timestamp']]}
#         ]
#     }
#     mock_values.batchGet.return_value = mock_batch_get
    
#     # Configure other methods
#     mock_values.clear.return_value.execute.return_value = {}
#     mock_values.update.return_value.execute.return_value = {'updatedCells': 1}
#     mock_sheet.values.return_value = mock_values
#     mock_service.spreadsheets.return_value = mock_sheet
    
#     with patch('google.oauth2.service_account.Credentials.from_service_account_file', return_value=mock_creds), \
#          patch('googleapiclient.discovery.build', return_value=mock_service):
#         assert save_to_sheets(test_data, 'test_sheet_id') == True

def test_save_to_sheets_input_validation():
    with pytest.raises(Exception) as exc_info:
        save_to_sheets(None, 'sheet_id')
    assert "Error saving to Google Sheets: Invalid or empty data" in str(exc_info.value)
    
    with pytest.raises(Exception) as exc_info:
        save_to_sheets([], 'sheet_id')
    assert "Error saving to Google Sheets: Invalid or empty data" in str(exc_info.value)
    
    with pytest.raises(Exception) as exc_info:
        save_to_sheets([{'test': 'data'}], '')
    assert "Error saving to Google Sheets: Invalid spreadsheet ID" in str(exc_info.value)

def test_save_to_sheets_validation():
    with pytest.raises(Exception) as exc_info:
        save_to_sheets([], 'sheet_id')
    assert "Error saving to Google Sheets: Invalid or empty data" in str(exc_info.value)
    
    with pytest.raises(Exception) as exc_info:
        save_to_sheets(None, 'sheet_id')
    assert "Error saving to Google Sheets: Invalid or empty data" in str(exc_info.value)
    
    with pytest.raises(Exception) as exc_info:
        save_to_sheets([{'test': 'data'}], '')
    assert "Error saving to Google Sheets: Invalid spreadsheet ID" in str(exc_info.value)

def test_save_to_sheets_api_error():
    test_data = [{
        'Title': 'Test Product',
        'Price': 160000,
        'Rating': 4.5,
        'Colors': 3,
        'Size': 'M',
        'Gender': 'Unisex',
        'timestamp': '2024-01-01 00:00:00'
    }]
    
    mock_sheet = MagicMock()
    mock_sheet.values.return_value.clear.side_effect = Exception("API Error")
    mock_service = MagicMock()
    mock_service.spreadsheets.return_value = mock_sheet
    
    with patch('google.oauth2.service_account.Credentials.from_service_account_file'), \
         patch('googleapiclient.discovery.build', return_value=mock_service), \
         pytest.raises(Exception):
        save_to_sheets(test_data, 'test_sheet_id')

def test_save_to_sheets_clear_error():
    test_data = [{
        'Title': 'Test Product',
        'Price': 160000,
        'Rating': 4.5,
        'Colors': 3,
        'Size': 'M',
        'Gender': 'Unisex',
        'timestamp': '2024-01-01 00:00:00'
    }]
    
    mock_sheet = MagicMock()
    mock_values = MagicMock()
    mock_values.clear.return_value.execute.side_effect = Exception("Clear error")
    mock_sheet.values.return_value = mock_values
    
    mock_service = MagicMock()
    mock_service.spreadsheets.return_value = mock_sheet
    
    with patch('google.oauth2.service_account.Credentials.from_service_account_file'), \
         patch('googleapiclient.discovery.build', return_value=mock_service), \
         pytest.raises(Exception):
        save_to_sheets(test_data, 'test_sheet_id')

def test_save_to_sheets_update_error():
    test_data = [{
        'Title': 'Test Product',
        'Price': 160000,
        'Rating': 4.5,
        'Colors': 3,
        'Size': 'M',
        'Gender': 'Unisex',
        'timestamp': '2024-01-01 00:00:00'
    }]
    
    mock_sheet = MagicMock()
    mock_values = MagicMock()
    mock_values.clear.return_value.execute.return_value = {}
    mock_values.update.return_value.execute.side_effect = Exception("Update error")
    mock_sheet.values.return_value = mock_values
    
    mock_service = MagicMock()
    mock_service.spreadsheets.return_value = mock_sheet
    
    with patch('google.oauth2.service_account.Credentials.from_service_account_file'), \
         patch('googleapiclient.discovery.build', return_value=mock_service), \
         pytest.raises(Exception):
        save_to_sheets(test_data, 'test_sheet_id')

def test_save_to_sheets_execute_error():
    test_data = [{
        'Title': 'Test Product',
        'Price': 160000,
        'Rating': 4.5,
        'Colors': 3,
        'Size': 'M',
        'Gender': 'Unisex',
        'timestamp': '2024-01-01 00:00:00'
    }]
    
    mock_sheet = MagicMock()
    mock_values = MagicMock()
    mock_values.clear.return_value.execute.return_value = {}
    mock_values.update.return_value.execute.side_effect = Exception("Execute error")
    mock_sheet.values.return_value = mock_values
    
    mock_service = MagicMock()
    mock_service.spreadsheets.return_value = mock_sheet
    
    with patch('google.oauth2.service_account.Credentials.from_service_account_file'), \
         patch('googleapiclient.discovery.build', return_value=mock_service), \
         pytest.raises(Exception) as exc_info:
        save_to_sheets(test_data, 'test_sheet_id')
    
    assert "Error saving to Google Sheets" in str(exc_info.value)
