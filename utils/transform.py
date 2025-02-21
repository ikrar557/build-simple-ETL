def transform_data(data):
    try:
        if not data:
            raise ValueError("Input data is empty")
            
        transformed_data = []
        seen_titles = set()
        
        for item in data:
            if not item.get('Title') or item.get('Title') == 'Unknown Product':
                print(f"Skipping invalid title: {item.get('Title')}")
                continue
                
            if item.get('Title') in seen_titles:
                print(f"Skipping duplicate title: {item.get('Title')}")
                continue
                
            try:
                transformed_item = {
                    'Title': str(item.get('Title', '')).strip(),
                    'Price': round(float(item.get('Price', 0)) * 16000, 2),  # USD to IDR
                    'Rating': float(item.get('Rating', 0)),
                    'Colors': int(str(item.get('Colors', '0')).split()[0]),
                    'Size': str(item.get('Size', '')).strip(),
                    'Gender': str(item.get('Gender', '')).strip(),
                    'timestamp': str(item.get('timestamp', ''))
                }
                
                if (transformed_item['Title'] and 
                    transformed_item['Price'] > 0 and 
                    0 <= transformed_item['Rating'] <= 5 and 
                    transformed_item['Colors'] > 0 and 
                    transformed_item['Size'] and 
                    transformed_item['Gender']):
                    
                    seen_titles.add(transformed_item['Title'])
                    transformed_data.append(transformed_item)
                    
            except (ValueError, TypeError) as e:
                continue 
            
        if not transformed_data:
            raise ValueError("No valid data after transformation")
            
        return transformed_data
    except Exception as e:
        raise Exception(f"Error during transformation: {str(e)}")