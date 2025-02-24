import pytest
from unittest.mock import patch, MagicMock
from utils.extract.scraper import scrape_main

def test_scrape_main_success():
    mock_html = '''
    <div class="collection-card">
        <h3 class="product-title">Test Product</h3>
        <span class="price">$10.00</span>
        <p>Rating: ⭐4.5/5</p>
        <p>Colors: 3 available</p>
        <p>Size: M</p>
        <p>Gender: Unisex</p>
    </div>
    <div class="collection-card">
        <h3 class="product-title">Test Product 2</h3>
        <span class="price">$20.00</span>
        <p>Rating: ⭐4.0/5</p>
        <p>Colors: 2 available</p>
        <p>Size: L</p>
        <p>Gender: Men</p>
    </div>
    <div class="collection-card">
        <h3 class="product-title">Test Product 3</h3>
        <span class="price">$30.00</span>
        <p>Rating: ⭐3.5/5</p>
        <p>Colors: 4 available</p>
        <p>Size: S</p>
        <p>Gender: Women</p>
    </div>
    '''
    
    with patch('requests.get') as mock_get:
        mock_get.return_value = MagicMock(
            text=mock_html,
            status_code=200,
            raise_for_status=MagicMock()
        )
        
        result = scrape_main()
        assert len(result) == 3

def test_scrape_main_network_error():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception('Network error')
        
        with pytest.raises(Exception) as exc_info:
            scrape_main()
        assert "Error during extraction: Network error" in str(exc_info.value)

def test_scrape_main_http_error():
    with patch('requests.get') as mock_get:
        mock_get.return_value = MagicMock(
            status_code=404,
            raise_for_status=MagicMock(side_effect=Exception("404 Client Error"))
        )
        
        with pytest.raises(Exception) as exc_info:
            scrape_main()
        assert "Error during extraction: 404 Client Error" in str(exc_info.value) 

def test_scrape_main_malformed_data():
    mock_html = '''
    <div class="collection-card">
        <h3 class="product-title">Test Product</h3>
        <span class="price">$invalid</span>
    </div>
    '''
    
    with patch('requests.get') as mock_get:
        mock_get.return_value = MagicMock(
            text=mock_html,
            status_code=200,
            raise_for_status=MagicMock()
        )
        
        with pytest.raises(Exception) as exc_info:
            scrape_main()
        assert "Error during extraction: No products found across all pages" in str(exc_info.value)

def test_scrape_main_empty_response():
    with patch('requests.get') as mock_get:
        mock_get.return_value = MagicMock(
            text='',
            status_code=200,
            raise_for_status=MagicMock()
        )
        
        with pytest.raises(Exception) as exc_info:
            scrape_main()
        assert "Empty response from server" in str(exc_info.value)

def test_scrape_main_no_products():
    with patch('requests.get') as mock_get:
        mock_get.return_value = MagicMock(
            text='<div>No products</div>',
            status_code=200,
            raise_for_status=MagicMock()
        )
        
        with pytest.raises(Exception) as exc_info:
            scrape_main()
        assert "No product cards found" in str(exc_info.value)

def test_scrape_main_invalid_product():
    mock_html = '''
    <div class="collection-card">
        <h3 class="product-title"></h3>
        <span class="price">invalid</span>
    </div>
    '''
    
    with patch('requests.get') as mock_get:
        mock_get.return_value = MagicMock(
            text=mock_html,
            status_code=200,
            raise_for_status=MagicMock()
        )
        
        with pytest.raises(Exception) as exc_info:
            scrape_main()
        assert "No products found" in str(exc_info.value)

def test_scrape_main():
    mock_html = '''
        <div class="collection-card">
            <h3 class="product-title">Test Product</h3>
            <span class="price">$100</span>
            <p>Rating: ⭐4.5/5</p>
            <p>Colors: 3 available</p>
            <p>Size: M</p>
            <p>Gender: Unisex</p>
        </div>
    '''
    
    with patch('requests.get') as mock_get:
        mock_get.return_value = MagicMock(
            text=mock_html,
            raise_for_status=MagicMock()
        )
        
        result = scrape_main()
        assert len(result) > 0
        assert result[0]['Title'] == 'Test Product'
        assert result[0]['Price'] == 100.0

def test_scrape_main_error():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("Network error")
        with pytest.raises(Exception):
            scrape_main()

def test_scrape_main_partial_data():
    mock_html = '''
    <div class="collection-card">
        <h3 class="product-title">Test Product</h3>
        <span class="price">$10.00</span>
        <!-- Missing Rating -->
        <!-- Missing Colors -->
        <p>Size: M</p>
        <p>Gender: Unisex</p>
    </div>
    '''
    
    with patch('requests.get') as mock_get:
        mock_get.return_value = MagicMock(
            text=mock_html,
            status_code=200,
            raise_for_status=MagicMock()
        )
        
        result = scrape_main()
        assert len(result) == 1
        assert result[0]['Rating'] == 0.0
        assert result[0]['Colors'] == 0

def test_scrape_main_missing_elements():
    mock_html = '''
    <div class="collection-card">
        <h3 class="product-title">Test Product</h3>
        <!-- Missing price -->
        <p>Rating: ⭐4.5/5</p>
        <p>Colors: 3 available</p>
        <p>Size: M</p>
        <p>Gender: Unisex</p>
    </div>
    '''
    
    with patch('requests.get') as mock_get:
        mock_get.return_value = MagicMock(
            text=mock_html,
            status_code=200,
            raise_for_status=MagicMock()
        )
        
        with pytest.raises(Exception) as exc_info:
            scrape_main()
        assert "Error during extraction: No products found across all pages" in str(exc_info.value)