def convert_price_to_idr(price, rate=16000):
    return round(float(price) * rate, 2)

def clean_string(value):
    return str(value).strip()

def parse_colors(colors):
    return int(str(colors).split()[0])

def parse_rating(rating):
    return float(rating)