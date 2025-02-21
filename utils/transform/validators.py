def validate_item_structure(item):
    return isinstance(item, dict)

def validate_title(title):
    return bool(title) and title != 'Unknown Product'

def validate_transformed_item(item):
    return (bool(item['Title']) and 
            item['Price'] > 0 and 
            0 <= item['Rating'] <= 5 and 
            item['Colors'] > 0 and 
            bool(item['Size']) and 
            bool(item['Gender']))  # Changed to bool() for string validation