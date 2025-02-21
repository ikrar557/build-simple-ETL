import pandas as pd

def save_to_csv(data, filename='products.csv'):
    if not filename.endswith('.csv'):
        filename = f"{filename}.csv"
        
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    return True