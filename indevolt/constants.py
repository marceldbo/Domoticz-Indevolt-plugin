"""
INDEVOLT cJSON Tag Definitions
Semantic mapping layer for Domoticz plugin
"""

# -----------------------------
# IDENTITY
# -----------------------------
SN = "0"

# -----------------------------
# SYSTEM / MODE
# -----------------------------
WORKING_MODE_STATE = "7101"
WORKING_MODE_SETTING = "47005"
CHARGING_STATE = "6001"
BYPASS_MODE_SETTING = "7266"
LIGHT_MODE_SETTING = "7265"

# -----------------------------
# BATTERY CORE
# -----------------------------
BATTERY_POWER = "6000"
BATTERY_SOC = "6002"

# -----------------------------
# POWER FLOWS (W)
# -----------------------------
TOTAL_INPUT_POWER = "2101"
TOTAL_OUTPUT_POWER = "2108"
BYPASS_POWER = "667"

# -----------------------------
# ENERGY FLOWS (kWh)
# -----------------------------
TOTAL_INPUT_ENERGY = "2107"
TOTAL_OUTPUT_ENERGY = "2104"

BATTERY_DAILY_CHARGE = "6004"
BATTERY_DAILY_DISCHARGE = "6005"

BATTERY_TOTAL_CHARGE = "6006"
BATTERY_TOTAL_DISCHARGE = "6007"

# -----------------------------
# GRID
# -----------------------------
GRID_VOLTAGE = "2600"
GRID_FREQUENCY = "2612"

# -----------------------------
# SYSTEM LIMITS
# -----------------------------
BACKUP_SOC = "6105"
RATED_CAPACITY = "142"

# -----------------------------
# BYPASS
# -----------------------------
BYPASS_ENABLE = "680"

# -----------------------------
# SENSOR
# -----------------------------
BATTERY_TEMPERATURE = "9012"

# -----------------------------
# Return value mappings
# -----------------------------
WORKING_MODE_STATE_MAP = {
    1: "Self-consumed Prioritized",
    4: "Real-time Control",
    5: "Charge/Discharge Schedule",   
}

CHARGING_STATE_MAP = {
    1000: "Static",
    1001: "Charging",
    1002: "Discharging",
}

BYPASS_MODE_SETTING_MAP = {
    0: "Off",
    1: "On",
}

LIGHT_MODE_SETTING_MAP = {
    0: "Off",
    1: "On",
}

WORKING_MODE_SETTING_MAP = {
    1: "Self-consumed Prioritized",
    4: "Real-time Control",
    5: "Charge/Discharge Schedule",   
}

# -----------------------------
# GROUPS (for API requests)
# -----------------------------
POWER_TAGS = [
    BATTERY_POWER,
    TOTAL_INPUT_POWER,
    TOTAL_OUTPUT_POWER,
    BYPASS_POWER,
]

ENERGY_TAGS = [
    TOTAL_INPUT_ENERGY,
    TOTAL_OUTPUT_ENERGY,
    BATTERY_DAILY_CHARGE,
    BATTERY_DAILY_DISCHARGE,
    BATTERY_TOTAL_CHARGE,
    BATTERY_TOTAL_DISCHARGE,
]

STATE_TAGS = [
    SN,
    WORKING_MODE_STATE,
    CHARGING_STATE,
    BYPASS_MODE_SETTING,
    LIGHT_MODE_SETTING,
]

GRID_TAGS = [
    GRID_VOLTAGE,
    GRID_FREQUENCY,
]

BATTERY_TAGS = [
    BATTERY_SOC,
    BACKUP_SOC,
    RATED_CAPACITY,
    BATTERY_TEMPERATURE,
]

ALL_TAGS = (
    POWER_TAGS +
    ENERGY_TAGS +
    STATE_TAGS +
    GRID_TAGS +
    BATTERY_TAGS
)
