"""
INDEVOLT Domoticz Plugin
Constants and device definitions

Version 2.1.0
"""

# ========================================================
# INDEVOLT REGISTER TAGS
# ==========================================================

TAG_SERIAL_NUMBER = 0

TAG_WORKING_MODE = 7101
TAG_CHARGING_STATE = 6001

TAG_BATTERY_POWER = 6000
TAG_BATTERY_SOC = 6002

TAG_TOTAL_AC_INPUT_POWER = 2101
TAG_TOTAL_AC_OUTPUT_POWER = 2108

TAG_TOTAL_INPUT_ENERGY = 2107
TAG_TOTAL_OUTPUT_ENERGY = 2104

TAG_DAILY_CHARGE = 6004
TAG_DAILY_DISCHARGE = 6005

TAG_TOTAL_CHARGE = 6006
TAG_TOTAL_DISCHARGE = 6007

TAG_BACKUP_SOC = 6105
TAG_RATED_CAPACITY = 142

TAG_BYPASS_ENABLE = 680
TAG_BYPASS_POWER = 667

TAG_GRID_VOLTAGE = 2600
TAG_GRID_FREQUENCY = 2612

TAG_BATTERY_TEMPERATURE = 9012
TAG_LIGHT_ENABLE = 7171

# ==========================================================
# SETDATA REGISTERS
# ==========================================================

SET_WORKING_MODE = 47005
SET_CHARGING_STATE = 47015

SET_BYPASS_ENABLE = 7266
SET_LIGHT_ENABLE = 7265

# ==========================================================
# DECODING TABLES
# ==========================================================

WORKING_MODE_MAP = {
    1: "Self-consumed Prioritized",
    4: "Real-time Control",
    5: "Charge/Discharge Schedule",
}

WORKING_MODE_LEVELS = {
    1: 0,
    4: 10,
    5: 20,
}

LEVEL_TO_WORKING_MODE = {
    0: 1,
    10: 4,
    20: 5,
}

CHARGING_STATE_MAP = {
    1000: "Static (Stand-by)",
    1001: "Charging",
    1002: "Discharging",
}

CHARGING_STATE_LEVELS = {
    1000: 0,
    1001: 10,
    1002: 20,
}

LEVEL_TO_CHARGING_STATE = {
    0: 0,
    10: 1,
    20: 2,
}

# ==========================================================
# API POLLING LIST
# ==========================================================

POLL_TAGS = [
    TAG_SERIAL_NUMBER,

    TAG_WORKING_MODE,
    TAG_CHARGING_STATE,

    TAG_BATTERY_POWER,
    TAG_BATTERY_SOC,

    TAG_TOTAL_AC_INPUT_POWER,
    TAG_TOTAL_AC_OUTPUT_POWER,

    TAG_TOTAL_INPUT_ENERGY,
    TAG_TOTAL_OUTPUT_ENERGY,

    TAG_DAILY_CHARGE,
    TAG_DAILY_DISCHARGE,

    TAG_TOTAL_CHARGE,
    TAG_TOTAL_DISCHARGE,

    TAG_BACKUP_SOC,
    TAG_RATED_CAPACITY,

    TAG_BYPASS_ENABLE,
    TAG_BYPASS_POWER,

    TAG_GRID_VOLTAGE,
    TAG_GRID_FREQUENCY,

    TAG_BATTERY_TEMPERATURE,
    TAG_LIGHT_ENABLE,
]

# ==========================================================
# DEVICE DEFINITIONS
#
# Each entry:
#
# tag:
#   unit       = Domoticz device unit
#   name       = device name
#   create     = exact Domoticz.Device parameters
#
# ==========================================================

DEVICE_DEFINITIONS = {

    TAG_SERIAL_NUMBER: {
        "unit": 1,
        "name": "Serial Number",
        "create": {
            "Type": 243,
            "Subtype": 19,
            "Used": 0,
        },
    },

    TAG_WORKING_MODE: {
        "unit": 2,
        "name": "Mode",
        "create": {
            "Type": 244,
            "Subtype": 62,
            "Switchtype": 18,
            "Options": {
                "LevelNames":
                    "Self-consumed Prioritized|"
                    "Real-time Control|"
                    "Charge/Discharge Schedule",
        
                "LevelActions":
                    "|||",
        
                "LevelOffHidden":
                "true",
        
                "SelectorStyle":
                "1"
            },
            "Used": 1,
        },

    },
        
    TAG_CHARGING_STATE: {
        "unit": 3,
        "name": "Charging state",
        "create": {
            "Type": 244,
            "Subtype": 62,
            "Switchtype": 18,
            "Options": {
                "LevelNames":
                    "Static (Stand-by)|"
                    "Charging|"
                    "Discharging",
        
                "LevelActions":
                    "|||",
        
                "LevelOffHidden":
                "true",
        
                "SelectorStyle":
                "1"
            },
            "Used": 1,
        },

    },
    
    TAG_BATTERY_POWER: {
        "unit": 4,
        "name": "Battery Power",
        "create": {
            "Type": 248,
            "Subtype": 1,
            "Used": 1,
        },
    },

    TAG_BATTERY_SOC: {
        "unit": 5,
        "name": "Battery SOC",
        "create": {
            "Type": 243,
            "Subtype": 6,
            "Used": 1,
        },
    },

    TAG_TOTAL_AC_INPUT_POWER: {
        "unit": 6,
        "name": "Total AC Input Power",
        "create": {
            "Type": 248,
            "Subtype": 1,
            "Used": 0,
        },
    },

    TAG_TOTAL_AC_OUTPUT_POWER: {
        "unit": 7,
        "name": "Total AC Output Power",
        "create": {
            "Type": 248,
            "Subtype": 1,
            "Used": 0,
        },
    },

    TAG_TOTAL_INPUT_ENERGY: {
        "unit": 8,
        "name": "Total Input Energy",
        "custom_unit": "kWh",
        "create": {
            "Type": 243,
            "Subtype": 31,
            "Options": {
                "Custom": "1;kWh",
            },
            "Used": 0,
        },
    },

    TAG_TOTAL_OUTPUT_ENERGY: {
        "unit": 9,
        "name": "Total Output Energy",
        "custom_unit": "kWh",
        "create": {
            "Type": 243,
            "Subtype": 31,
            "Options": {
                "Custom": "1;kWh",
            },
            "Used": 0,
        },
    },

    TAG_DAILY_CHARGE: {
        "unit": 10,
        "name": "Battery Daily Charge",
        "custom_unit": "kWh",
        "create": {
            "Type": 243,
            "Subtype": 31,
            "Options": {
                "Custom": "1;kWh",
            },
            "Used": 0,
        },
    },

    TAG_DAILY_DISCHARGE: {
        "unit": 11,
        "name": "Battery Daily Discharge",
        "custom_unit": "kWh",
        "create": {
            "Type": 243,
            "Subtype": 31,
            "Options": {
                "Custom": "1;kWh",
            },
            "Used": 0,
        },
    },

    TAG_TOTAL_CHARGE: {
        "unit": 12,
        "name": "Battery Total Charge",
        "custom_unit": "kWh",
        "create": {
            "Type": 243,
            "Subtype": 31,
            "Options": {
                "Custom": "1;kWh",
            },
            "Used": 0,
        },
    },

    TAG_TOTAL_DISCHARGE: {
        "unit": 13,
        "name": "Battery Total Discharge",
        "custom_unit": "kWh",
        "create": {
            "Type": 243,
            "Subtype": 31,
            "Options": {
                "Custom": "1;kWh",
            },
            "Used": 0,
        },
    },

    TAG_BACKUP_SOC: {
        "unit": 14,
        "name": "Backup SOC",
        "create": {
            "Type": 243,
            "Subtype": 6,
            "Used": 0,
        },
    },

    TAG_RATED_CAPACITY: {
        "unit": 15,
        "name": "Rated Capacity",
        "create": {
            "Type": 243,
            "Subtype": 31,
            "Options": {
                "Custom": "1;kWh",
            },
            "Used": 1,
        },
    },

    TAG_BYPASS_ENABLE: {
        "unit": 16,
        "name": "Bypass Enabled",
        "create": {
            "Type": 244,
            "Subtype": 62,
            "Switchtype": 0,
            "Used": 1,
        },
    },

    TAG_BYPASS_POWER: {
        "unit": 17,
        "name": "Bypass Power",
        "create": {
            "Type": 248,
            "Subtype": 1,
            "Used": 0,
        },
    },

    TAG_GRID_VOLTAGE: {
        "unit": 18,
        "name": "Grid Voltage",
        "create": {
            "Type": 243,
            "Subtype": 8,
            "Used": 0,
        },
    },

    TAG_GRID_FREQUENCY: {
        "unit": 19,
        "name": "Grid Frequency",
        "create": {
            "Type": 243,
            "Subtype": 31,
            "Options": {
                "Custom": "1;Hz",
            },
            "Used": 0,
        },
    },

    TAG_BATTERY_TEMPERATURE: {
        "unit": 20,
        "name": "Battery Temperature",
        "create": {
            "Type": 80,
            "Subtype": 5,
            "Used": 1,
        },
    },
    
    TAG_LIGHT_ENABLE: {
        "unit": 21,
        "name": "Light Enabled",
        "create": {
            "Type": 244,
            "Subtype": 62,
            "Switchtype": 0,
            "Used": 1,
        },
    },
}
