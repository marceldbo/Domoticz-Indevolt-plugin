"""
INDEVOLT Domoticz Plugin
Helper functions

Version 2.0.0
"""

import Domoticz

from .constants import (
    WORKING_MODE_LEVELS,
    LEVEL_TO_WORKING_MODE,
)


# ==========================================================
# SAFE CONVERSION FUNCTIONS
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


def format_number(value, decimals=2):

    """
    Format numeric values for Domoticz.
    """

    try:

        return f"{float(value):.{decimals}f}"

    except Exception:

        return str(value)



# ==========================================================
# WORKING MODE CONVERSION
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
# DEBUG LOGGING
# ==========================================================


DEBUG = False



def set_debug(enabled):

    global DEBUG

    DEBUG = enabled



def log_debug(message):

    if DEBUG:

        Domoticz.Log(
            f"INDEVOLT DEBUG: {message}"
        )



def log_error(message):

    Domoticz.Error(
        f"INDEVOLT ERROR: {message}"
    )



# ==========================================================
# DATA VALIDATION
# ==========================================================


def valid_api_response(data):

    """
    Validate INDEVOLT GetData response.

    Expected:

    {
        "6000":0,
        "6001":1000,
        "7101":1
    }

    """

    if not isinstance(data, dict):

        log_error(
            f"Invalid API response type: {type(data)}"
        )

        return False


    return True
