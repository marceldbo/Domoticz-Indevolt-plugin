def safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def watt_to_kw(w):
    return round(float(w) / 1000.0, 3)
