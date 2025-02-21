def convert_price_to_idr(price, rate=16000):
    try:
        if not isinstance(rate, (int, float)) or rate <= 0:
            raise ValueError("Invalid exchange rate")
        return round(float(price) * rate, 2)
    except (ValueError, TypeError):
        return 0.0

def clean_string(value):
    try:
        return str(value).strip()
    except (AttributeError, TypeError):
        return ''

def parse_colors(colors):
    try:
        value = str(colors).split()[0]
        result = int(value)
        return max(0, result)
    except (ValueError, IndexError, AttributeError):
        return 0

def parse_rating(rating):
    try:
        result = float(rating)
        return max(0.0, min(5.0, result))
    except (ValueError, TypeError):
        return 0.0