def validate_item_structure(item):
    try:
        if item is None:
            return False
        if not isinstance(item, dict):
            return False
        if not item:
            return False
        return True
    except Exception:
        return False

def validate_title(title):
    try:
        if title is None:
            return False
        if not isinstance(title, str):
            return False
            
        title = title.strip()
        if not title:
            return False
        if title == 'Unknown Product':
            return False
        if len(title) < 3:
            return False
            
        return True
    except Exception:
        return False

def validate_transformed_item(item):
    try:
        required_fields = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender']
        
        if not all(field in item for field in required_fields):
            return False
            
        return (bool(item['Title'].strip()) and 
                isinstance(item['Price'], (int, float)) and item['Price'] > 0 and 
                isinstance(item['Rating'], (int, float)) and 0 <= item['Rating'] <= 5 and 
                isinstance(item['Colors'], int) and item['Colors'] > 0 and 
                isinstance(item['Size'], str) and bool(item['Size'].strip()) and 
                isinstance(item['Gender'], str) and bool(item['Gender'].strip()))
    except (KeyError, AttributeError, TypeError):
        return False