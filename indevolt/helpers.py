"""
INDEVOLT Domoticz Plugin - Helpers
Safe conversions + formatting utilities
"""

import Domoticz


# =========================================================
# SAFE TYPE CONVERSION
# =========================================================

def safe_int(value, default=0):
    try:
        if value is None:
            return default
        return int(value)
    except Exception:
        return default


def safe_float(value, default=0.0):
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


# =========================================================
# SAFE STRING
# =========================================================

def safe_str(value, default=""):
    try:
        if value is None:
            return default
        return str(value)
    except Exception:
        return default


# =========================================================
# DEVICE VALUE FORMATTING
# =========================================================

def format_value(value, decimals=2):
    """
    Converts numeric values into clean Domoticz strings
    """
    try:
        v = float(value)
        return f"{v:.{decimals}f}"
    except Exception:
        return str(value)


# =========================================================
# SELECTOR SWITCH MAPPING HELPERS
# =========================================================

def mode_to_level(mode):
    """
    INDEVOLT → Domoticz selector level
    """
    mapping = {
        1: 10,  # Self-consumed
        4: 20,  # Real-time
        5: 30,  # Schedule
    }
    return mapping.get(mode, 0)


def level_to_mode(level):
    """
    Domoticz selector level → INDEVOLT
    """
    mapping = {
        10: 1,
        20: 4,
        30: 5,
    }
    return mapping.get(level)


# =========================================================
# LOGGING WRAPPERS
# =========================================================

def log_debug(msg):
    Domoticz.Log(f"[INDEVOLT] {msg}")


def log_error(msg):
    Domoticz.Error(f"[INDEVOLT] {msg}")


# =========================================================
# RESPONSE VALIDATION
# =========================================================

def validate_response(data):
    """
    Ensures API response is usable
    """
    if not isinstance(data, dict):
        log_error(f"Invalid API response type: {type(data)}")
        return False
    return True
