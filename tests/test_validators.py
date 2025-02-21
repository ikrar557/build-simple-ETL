import pytest
from utils.transform.validators import validate_item_structure, validate_title, validate_transformed_item

def test_validate_item_structure():
    assert validate_item_structure({'key': 'value'}) == True
    assert validate_item_structure({'Title': 'Test'}) == True
    assert validate_item_structure({}) == False
    assert validate_item_structure([]) == False
    assert validate_item_structure(None) == False
    assert validate_item_structure('string') == False
    assert validate_item_structure(123) == False

def test_validate_transformed_item():
    valid_item = {
        'Title': 'Test Product',
        'Price': 160000,
        'Rating': 4.5,
        'Colors': 3,
        'Size': 'M',
        'Gender': 'Unisex',
        'timestamp': '2024-01-01 00:00:00'
    }
    
    assert validate_transformed_item(valid_item) == True

    invalid_items = [
        {**valid_item, 'Title': ''},
        {**valid_item, 'Price': 0},
        {**valid_item, 'Rating': -1},
        {**valid_item, 'Rating': 5.1},
        {**valid_item, 'Colors': 0},
        {**valid_item, 'Size': ''},
        {**valid_item, 'Gender': ''},
        {},
        {'Title': 'Test'}, 
        None
    ]
    
    for item in invalid_items:
        assert validate_transformed_item(item) == False

def test_validate_title():
    # Valid cases
    assert validate_title('Valid Title') == True
    assert validate_title('ABC') == True 
    assert validate_title('  Random Title  ') == True 
    
    # Invalid cases
    assert validate_title('') == False
    assert validate_title('  ') == False 
    assert validate_title('AB') == False 
    assert validate_title('Unknown Product') == False
    assert validate_title(None) == False
    assert validate_title(123) == False
    assert validate_title(['title']) == False
    assert validate_title({'title': 'value'}) == False
