import pytest
from utils.transform.transform import transform_data

def test_transform_data_valid():
    test_data = [{
        'Title': 'Test Product',
        'Price': 10.0,
        'Rating': 4.5,
        'Colors': 3,
        'Size': 'M',
        'Gender': 'Unisex',
        'timestamp': '2024-01-01 00:00:00'
    }]
    
    result = transform_data(test_data)
    assert len(result) == 1
    assert result[0]['Price'] == 160000  # 10 * 16000

def test_transform_data_invalid():
    invalid_data = [
        None,
        {},
        {'Title': 'Unknown Product'},
        {'Title': 'Test', 'Price': 0},
    ]
    
    result = transform_data(invalid_data)
    assert len(result) == 0

def test_transform_data_all_invalid():
    invalid_data = [
        {'Title': '', 'Price': 0, 'Rating': 6, 'Colors': 0, 'Size': '', 'Gender': ''},
        {'Title': 'Unknown Product', 'Price': -1, 'Rating': -1, 'Colors': -1, 'Size': '', 'Gender': ''}
    ]
    
    result = transform_data(invalid_data)
    assert len(result) == 0

def test_transform_data_value_error():
    invalid_data = [
        {'Title': 'Test', 'Price': 'invalid', 'Rating': 4.5, 'Colors': 3, 'Size': 'M', 'Gender': 'Unisex'},
    ]
    
    result = transform_data(invalid_data)
    assert len(result) == 0

def test_transform_data_duplicates():
    duplicate_data = [
        {'Title': 'Same Product', 'Price': 10.0, 'Rating': 4.5, 'Colors': 3, 'Size': 'M', 'Gender': 'Unisex'},
        {'Title': 'Same Product', 'Price': 20.0, 'Rating': 4.5, 'Colors': 3, 'Size': 'M', 'Gender': 'Unisex'}
    ]
    
    result = transform_data(duplicate_data)
    assert len(result) == 1
    assert result[0]['Price'] == 160000  # First item's price should be used

def test_transform_data_empty():
    with pytest.raises(ValueError) as exc_info:  # Changed to ValueError
        transform_data([])
    assert "Empty input data" in str(exc_info.value)