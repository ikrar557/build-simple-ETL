def transform_data(data):
    try:
        if not isinstance(data, list):
            raise TypeError("Input data must be a list")
            
        if not data:
            raise ValueError("Input data is empty")
            
        transformed_data = []
        # Memberi tanda judul untuk menghindari duplikat
        seen_titles = set()
        invalid_count = 0
        
        for index, item in enumerate(data):
            # Memastikan struktur data valid
            if not isinstance(item, dict):
                print(f"Skipping item {index}: Not a dictionary")
                invalid_count += 1
                continue
            
            # Melakukan filter nillai yang invalid seperti "Unknown product" dan tidak ada atau null
            if not item.get('Title') or item.get('Title') == 'Unknown Product':
                print(f"Skipping invalid title at index {index}: {item.get('Title')}")
                invalid_count += 1
                continue
            
            # Skip title yang memiliki duplikat untuk memastikan data unik
            if item.get('Title') in seen_titles:
                print(f"Skipping duplicate title: {item.get('Title')}")
                continue
                
            try:
                transformed_item = {
                    'Title': str(item.get('Title', '')).strip(),
                    # Konversi USD ke IDR
                    'Price': round(float(item.get('Price', 0)) * 16000, 2),
                    'Rating': float(item.get('Rating', 0)),
                    'Colors': int(str(item.get('Colors', '0')).split()[0]),
                    'Size': str(item.get('Size', '')).strip(),
                    'Gender': str(item.get('Gender', '')).strip(),
                    'timestamp': str(item.get('timestamp', ''))
                }
                
                # Validasi semua field yang diperlukan memiliki nilai yang valid
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
            
        if invalid_count > 0:
            print(f"Warning: {invalid_count} items were invalid and skipped")
            
        if not transformed_data:
            raise ValueError("No valid data after transformation")
            
        return transformed_data
    except Exception as e:
        raise Exception(f"Error during transformation: {str(e)}")