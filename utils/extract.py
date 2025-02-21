import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_main():
    try:
        url = "https://fashion-studio.dicoding.dev/"
        try:
            response = requests.get(url, timeout=10)  # Add timeout
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch data: {str(e)}")
        
        if not response.text:
            raise ValueError("Empty response from server")
            
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []
        
        product_cards = soup.find_all('div', class_='collection-card')
        if not product_cards:
            raise ValueError("No product cards found on the page")
        
        for card in product_cards:
            try:
                title_elem = card.find('h3', class_='product-title')
                if not title_elem:
                    continue
                title = title_elem.text.strip()
                
                price_elem = card.find('span', class_='price')
                if not price_elem:
                    continue
                price = float(price_elem.text.strip().replace('$', ''))
                
                rating = 0.0
                rating_elem = card.find('p', text=lambda t: t and 'Rating:' in t)
                if rating_elem:
                    try:
                        rating_text = rating_elem.text.strip()
                        rating = float(rating_text.split('/')[0].split('⭐')[-1].strip())
                    except (ValueError, IndexError):
                        rating = 0.0
                
                colors = 0
                colors_elem = card.find('p', text=lambda t: t and 'Colors' in t)
                if colors_elem:
                    try:
                        colors_text = colors_elem.text.strip()
                        colors = int(colors_text.split()[0])
                    except (ValueError, IndexError):
                        colors = 0
                
                size = ''
                size_elem = card.find('p', text=lambda t: t and 'Size:' in t)
                if size_elem:
                    size = size_elem.text.split(':')[-1].strip()
                
                gender = ''
                gender_elem = card.find('p', text=lambda t: t and 'Gender:' in t)
                if gender_elem:
                    gender = gender_elem.text.split(':')[-1].strip()
                
                if title and price > 0:
                    product = {
                        'Title': title,
                        'Price': price,
                        'Rating': rating,
                        'Colors': colors,
                        'Size': size,
                        'Gender': gender
                    }
                    products.append(product)
                
            except Exception as e:
                print(f"Skipping product due to error: {str(e)}")
                continue
                
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
        for product in products:
            product['timestamp'] = timestamp
            
        if not products:
            raise Exception("No products found on the page")
            
        return products
    except Exception as e:
        raise Exception(f"Error during extraction: {str(e)}")