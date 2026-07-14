"""
INDEVOLT Domoticz Plugin
Helper functions

Version 2.0.0
"""

import Domoticz

from .constants import (
    CHARGING_STATE_MAP,
    CHARGING_STATE_LEVELS,
    LEVEL_TO_CHARGING_MODE,
    WORKING_MODE_MAP,
    WORKING_MODE_LEVELS,
    LEVEL_TO_WORKING_MODE,
)

# ==========================================================
# DEBUG HANDLING
# ==========================================================

DEBUG = False

def set_debug(enabled):

    global DEBUG
    DEBUG = bool(enabled)

def log_debug(message):

    if DEBUG:

        Domoticz.Log(
            f"INDEVOLT DEBUG: {message}"
        )

def log_info(message):

    Domoticz.Log(
        f"INDEVOLT: {message}"
    )

def log_error(message):

    Domoticz.Error(
        f"INDEVOLT ERROR: {message}"
    )

# ==========================================================
# SAFE CONVERSIONS
# ==========================================================

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

def safe_string(value, default=""):

    try:

        if value is None:
            return default

        return str(value)

    except Exception:

        return default

# ==========================================================
# VALUE FORMATTING
# ==========================================================

def format_value(value, decimals=2):

    """
    Format numeric values for Domoticz.

    Examples:

    3.540000 -> 3.54
    50.00000 -> 50

    """

    try:

        number = float(value)

        formatted = (
            f"{number:.{decimals}f}"
            .rstrip("0")
            .rstrip(".")
        )

        return formatted

    except Exception:

        return str(value)

# ==========================================================
# INDEVOLT STATE DECODING
# ==========================================================

def charging_state(value):

    """
    Convert:

    1000 -> Static (Stand-by)
    1001 -> Charging
    1002 -> Discharging

    """

    state = safe_int(value)

    return CHARGING_STATE_MAP.get(
        state,
        f"Unknown ({state})"
    )

def working_mode(value):

    """
    Convert:

    1 -> Self-consumed Prioritized
    4 -> Real-time Control
    5 -> Charge/Discharge Schedule

    """

    mode = safe_int(value)

    return WORKING_MODE_MAP.get(
        mode,
        f"Unknown ({mode})"
    )

# ==========================================================
# CHARGING STATE SELECTOR HANDLING
# ==========================================================

def charging_state_to_level(state):

    """
    INDEVOLT charging state -> Domoticz selector level

    0 -> 10
    1 -> 20
    2 -> 30
    """

    return CHARGING_STATE_LEVELS.get(
        safe_int(state),
        0
    )

def level_to_charging_state(level):

    """
    Domoticz selector level -> INDEVOLT charging state
    """

    return LEVEL_TO_CHARGING_STATE.get(
        safe_int(level)
    )

# ==========================================================
# WORKING MODE SELECTOR HANDLING
# ==========================================================

def working_mode_to_level(mode):

    """
    INDEVOLT mode -> Domoticz selector level

    1 -> 10
    4 -> 20
    5 -> 30
    """

    return WORKING_MODE_LEVELS.get(
        safe_int(mode),
        0
    )

def level_to_working_mode(level):

    """
    Domoticz selector level -> INDEVOLT mode
    """

    return LEVEL_TO_WORKING_MODE.get(
        safe_int(level)
    )

# ==========================================================
# API RESPONSE CHECK
# ==========================================================

def validate_response(data):

    """
    Verify INDEVOLT GetData response.

    Expected:

    {
        "6000":0,
        "6001":1000,
        "7101":1
    }

    """

    if not isinstance(data, dict):

        log_error(
            f"Invalid API response: {type(data)}"
        )

        return False


    return True
