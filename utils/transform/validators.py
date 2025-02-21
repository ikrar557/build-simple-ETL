def validate_item_structure(item):
    return isinstance(item, dict)

def validate_title(title):
    return bool(title) and title != 'Unknown Product'

def validate_transformed_item(item):
    return (item['Title'] and 
            item['Price'] > 0 and 
            0 <= item['Rating'] <= 5 and 
            item['Colors'] > 0 and 
            item['Size'] and 
            item['Gender'])