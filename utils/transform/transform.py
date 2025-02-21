from .validators import validate_item_structure, validate_title, validate_transformed_item
from .converters import convert_price_to_idr, clean_string, parse_colors, parse_rating

def transform_data(data):
    if not isinstance(data, list):
        raise TypeError("Input must be a list")
    
    if not data:
        raise ValueError("Empty input data") 
        
    transformed_data = []
    seen_titles = set()
    invalid_count = 0
    
    for index, item in enumerate(data):
        if not validate_item_structure(item):
            print(f"Skipping item {index}: Not a dictionary")
            invalid_count += 1
            continue
            
        title = item.get('Title')
        if not validate_title(title):
            print(f"Skipping invalid title at index {index}: {title}")
            invalid_count += 1
            continue
            
        if title in seen_titles:
            print(f"Skipping duplicate title: {title}")
            continue
            
        try:
            transformed_item = {
                'Title': clean_string(title),
                'Price': convert_price_to_idr(item.get('Price', 0)),
                'Rating': parse_rating(item.get('Rating', 0)),
                'Colors': parse_colors(item.get('Colors', '0')),
                'Size': clean_string(item.get('Size', '')),
                'Gender': clean_string(item.get('Gender', '')),
                'timestamp': clean_string(item.get('timestamp', ''))
            }
            
            if validate_transformed_item(transformed_item):
                seen_titles.add(transformed_item['Title'])
                transformed_data.append(transformed_item)
                
        except (ValueError, TypeError) as e:
            continue
            
    if invalid_count > 0:
        print(f"Warning: {invalid_count} items were invalid and skipped")
        
    return transformed_data