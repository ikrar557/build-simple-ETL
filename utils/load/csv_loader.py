import pandas as pd

def save_to_csv(data, filename='products.csv'):
    try:
        if not data or not isinstance(data, list):
            raise ValueError("Invalid or empty data")
            
        if not filename.endswith('.csv'):
            filename = f"{filename}.csv"
            
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        return True
        
    except (ValueError, TypeError) as e:
        raise ValueError(f"Error saving to CSV: {str(e)}")
    except Exception as e:
        raise Exception(f"Error saving to CSV: {str(e)}")