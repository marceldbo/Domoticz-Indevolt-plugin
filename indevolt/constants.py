"""
INDEVOLT Domoticz Plugin - Constants
Single source of truth for all registers and mappings
"""

# =========================================================
# INDEVOLT REGISTER TAGS
# =========================================================

TAG_SN = "0"

TAG_WORKING_MODE = "7101"
TAG_CHARGING_STATE = "6001"

TAG_BATTERY_POWER = "6000"
TAG_BATTERY_SOC = "6002"

TAG_GRID_INPUT_POWER = "2101"
TAG_GRID_OUTPUT_POWER = "2108"

TAG_GRID_INPUT_ENERGY = "2107"
TAG_GRID_OUTPUT_ENERGY = "2104"

TAG_BATTERY_DAILY_CHARGE = "6004"
TAG_BATTERY_DAILY_DISCHARGE = "6005"
TAG_BATTERY_TOTAL_CHARGE = "6006"
TAG_BATTERY_TOTAL_DISCHARGE = "6007"

TAG_BACKUP_SOC = "6105"
TAG_RATED_CAPACITY = "142"

TAG_BYPASS_ENABLE = "680"
TAG_BYPASS_POWER = "667"

TAG_GRID_VOLTAGE = "2600"
TAG_GRID_FREQUENCY = "2612"

TAG_BATTERY_TEMPERATURE = "1671"

# =========================================================
# WORKING MODE DECODING
# =========================================================

WORKING_MODE_MAP = {
    1: "Self-consumed Prioritized",
    4: "Real-time Control",
    5: "Charge/Discharge Schedule",
}

# =========================================================
# CHARGING STATE DECODING
# =========================================================

CHARGING_STATE_MAP = {
    1000: "Static",
    1001: "Charging",
    1002: "Discharging",
}

# =========================================================
# TAG LIST FOR POLLING (GetData)
# =========================================================

POLL_TAGS = [
    TAG_SN,
    TAG_WORKING_MODE,
    TAG_CHARGING_STATE,

    TAG_BATTERY_POWER,
    TAG_BATTERY_SOC,

    TAG_GRID_INPUT_POWER,
    TAG_GRID_OUTPUT_POWER,

    TAG_GRID_INPUT_ENERGY,
    TAG_GRID_OUTPUT_ENERGY,

    TAG_BATTERY_DAILY_CHARGE,
    TAG_BATTERY_DAILY_DISCHARGE,
    TAG_BATTERY_TOTAL_CHARGE,
    TAG_BATTERY_TOTAL_DISCHARGE,

    TAG_BACKUP_SOC,
    TAG_RATED_CAPACITY,

    TAG_BYPASS_ENABLE,
    TAG_BYPASS_POWER,

    TAG_GRID_VOLTAGE,
    TAG_GRID_FREQUENCY,

    TAG_BATTERY_TEMPERATURE,
]

# =========================================================
# DEVICE DEFINITIONS (Domoticz mapping)
# single source of truth for creation + updates
# =========================================================

DEVICE_DEFINITIONS = {
    TAG_SN: {
        "unit": 1,
        "name": "Indevolt Serial Number",
        "type": "Text",
    },

    TAG_WORKING_MODE: {
        "unit": 2,
        "name": "Working Mode",
        "type": "Selector",
        "decode": WORKING_MODE_MAP,
    },

    TAG_CHARGING_STATE: {
        "unit": 3,
        "name": "Charging State",
        "type": "Text",
        "decode": CHARGING_STATE_MAP,
    },

    TAG_BATTERY_POWER: {
        "unit": 4,
        "name": "Battery Power (W)",
        "type": "Usage",
    },

    TAG_BATTERY_SOC: {
        "unit": 5,
        "name": "Battery SOC (%)",
        "type": "Percentage",
    },

    TAG_GRID_INPUT_POWER: {
        "unit": 6,
        "name": "Grid Input Power (W)",
        "type": "Usage",
    },

    TAG_GRID_OUTPUT_POWER: {
        "unit": 7,
        "name": "Grid Output Power (W)",
        "type": "Usage",
    },

    TAG_GRID_INPUT_ENERGY: {
        "unit": 8,
        "name": "Grid Import Energy (kWh)",
        "type": "kWh",
    },

    TAG_GRID_OUTPUT_ENERGY: {
        "unit": 9,
        "name": "Grid Export Energy (kWh)",
        "type": "kWh",
    },

    TAG_BATTERY_DAILY_CHARGE: {
        "unit": 10,
        "name": "Battery Daily Charge (kWh)",
        "type": "kWh",
    },

    TAG_BATTERY_DAILY_DISCHARGE: {
        "unit": 11,
        "name": "Battery Daily Discharge (kWh)",
        "type": "kWh",
    },

    TAG_BATTERY_TOTAL_CHARGE: {
        "unit": 12,
        "name": "Battery Total Charge (kWh)",
        "type": "kWh",
    },

    TAG_BATTERY_TOTAL_DISCHARGE: {
        "unit": 13,
        "name": "Battery Total Discharge (kWh)",
        "type": "kWh",
    },

    TAG_BACKUP_SOC: {
        "unit": 14,
        "name": "Backup SOC (%)",
        "type": "Percentage",
    },

    TAG_RATED_CAPACITY: {
        "unit": 15,
        "name": "Rated Capacity (kWh)",
        "type": "Custom",
        "unit_label": "kWh",
    },

    TAG_BYPASS_ENABLE: {
        "unit": 16,
        "name": "Bypass Enable",
        "type": "Switch",
    },

    TAG_BYPASS_POWER: {
        "unit": 17,
        "name": "Bypass Power (W)",
        "type": "Usage",
    },

    TAG_GRID_VOLTAGE: {
        "unit": 18,
        "name": "Grid Voltage",
        "type": "Voltage",
    },

    TAG_GRID_FREQUENCY: {
        "unit": 19,
        "name": "Grid Frequency",
        "type": "Custom",
        "unit_label": "Hz",
    },

    TAG_BATTERY_TEMPERATURE: {
        "unit": 20,
        "name": "Battery Temperature (°C)",
        "type": "Temperature",
    },
}
