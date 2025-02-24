import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_main():
    try:
        all_products = []
        seen_titles = set()
        stats = {
            'total_cards': 0,
            'skipped_duplicates': 0,
            'invalid_products': 0,
            'missing_title': 0,
            'missing_price': 0,
            'processed_pages': 0,
            'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
        }
        
        base_url = "https://fashion-studio.dicoding.dev"
        page = 1
        consecutive_empty_pages = 0
        
        while page <= 50:
            try:
                if page == 1:
                    url = base_url
                else:
                    url = f"{base_url}/page{page}"
                
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                if not response.text:
                    raise ValueError("Empty response from server")
                    
                soup = BeautifulSoup(response.text, 'html.parser')
                product_cards = soup.find_all('div', class_='collection-card')
                
                if not product_cards:
                    raise ValueError("No product cards found on the page")
                
                stats['total_cards'] += len(product_cards)
                page_products_count = 0
                
                for card in product_cards:
                    try:
                        title_elem = card.find('h3', class_='product-title')
                        if not title_elem:
                            stats['missing_title'] += 1
                            continue
                        title = title_elem.text.strip()
                        
                        if title in seen_titles:
                            stats['skipped_duplicates'] += 1
                            continue
                        seen_titles.add(title)
                        
                        price_elem = card.find('span', class_='price')
                        if not price_elem:
                            stats['missing_price'] += 1
                            continue
                        
                        try:
                            price = float(price_elem.text.strip().replace('$', ''))
                        except ValueError:
                            stats['invalid_products'] += 1
                            continue
                        
                        rating = 0.0
                        rating_elem = card.find('p', string=lambda t: t and 'Rating:' in t)
                        if rating_elem:
                            try:
                                rating_text = rating_elem.text.strip()
                                rating = float(rating_text.split('/')[0].split('⭐')[-1].strip())
                            except (ValueError, IndexError):
                                rating = 0.0
                        
                        colors = 0
                        colors_elem = card.find('p', string=lambda t: t and 'Colors' in t)
                        if colors_elem:
                            try:
                                colors_text = colors_elem.text.strip()
                                colors = int(colors_text.split()[0])
                            except (ValueError, IndexError):
                                colors = 0
                        
                        size = ''
                        size_elem = card.find('p', string=lambda t: t and 'Size:' in t)
                        if size_elem:
                            size = size_elem.text.split(':')[-1].strip()
                        
                        gender = ''
                        gender_elem = card.find('p', string=lambda t: t and 'Gender:' in t)
                        if gender_elem:
                            gender = gender_elem.text.split(':')[-1].strip()
                        
                        if title and price > 0:
                            product = {
                                'Title': title,
                                'Price': price,
                                'Rating': rating,
                                'Colors': colors,
                                'Size': size,
                                'Gender': gender,
                                'Page': page,
                                'timestamp': stats['timestamp']
                            }
                            all_products.append(product)
                            page_products_count += 1
                        
                    except Exception as e:
                        stats['invalid_products'] += 1
                        print(f"Error processing product on page {page}: {str(e)}")
                        continue
                
                print(f"\nPage {page} Summary:")
                print(f"- Found {page_products_count} new unique products")
                stats['processed_pages'] += 1
                page += 1
                
            except requests.RequestException as e:
                raise Exception("Failed to fetch data")
            except Exception as e:
                raise
        
        print("\n=== Final Extraction Statistics ===")
        print(f"Total product cards found: {stats['total_cards']}")
        print(f"Successfully extracted products: {len(all_products)}")
        print(f"Skipped duplicate products: {stats['skipped_duplicates']}")
        print(f"Invalid/malformed products: {stats['invalid_products']}")
        print(f"Products missing title: {stats['missing_title']}")
        print(f"Products missing price: {stats['missing_price']}")
        print(f"Pages processed: {stats['processed_pages']}")
        print("================================\n")
            
        if not all_products:
            raise ValueError("No products found across all pages")
            
        return all_products
        
    except Exception as e:
        raise Exception(f"Error during extraction: {str(e)}")