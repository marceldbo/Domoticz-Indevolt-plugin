"""
INDEVOLT Domoticz Plugin
Constants and device definitions

Version 2.0.0
"""


# ==========================================================
# INDEVOLT REGISTER DEFINITIONS
# ==========================================================

TAG_SERIAL_NUMBER = "0"

TAG_WORKING_MODE = "7101"

TAG_BATTERY_POWER = "6000"
TAG_CHARGING_STATE = "6001"
TAG_BATTERY_SOC = "6002"

TAG_TOTAL_INPUT_POWER = "2101"
TAG_TOTAL_OUTPUT_POWER = "2108"

TAG_TOTAL_INPUT_ENERGY = "2107"
TAG_TOTAL_OUTPUT_ENERGY = "2104"

TAG_DAILY_CHARGE = "6004"
TAG_DAILY_DISCHARGE = "6005"

TAG_TOTAL_CHARGE = "6006"
TAG_TOTAL_DISCHARGE = "6007"

TAG_BACKUP_SOC = "6105"

TAG_RATED_CAPACITY = "142"

TAG_BYPASS_ENABLE = "680"
TAG_BYPASS_POWER = "667"

TAG_GRID_VOLTAGE = "2600"
TAG_GRID_FREQUENCY = "2612"

TAG_BATTERY_TEMPERATURE = "1671"


# ==========================================================
# SETDATA REGISTERS
# ==========================================================

SET_WORKING_MODE = 47005


# ==========================================================
# DECODING TABLES
# ==========================================================

CHARGING_STATE_MAP = {

    1000: "Static",
    1001: "Charging",
    1002: "Discharging",

}


WORKING_MODE_MAP = {

    1: "Self-consumed Prioritized",
    4: "Real-time Control",
    5: "Charge/Discharge Schedule",

}


# Domoticz Selector levels

WORKING_MODE_LEVELS = {

    1: 10,
    4: 20,
    5: 30,

}


# Reverse selector mapping

LEVEL_TO_WORKING_MODE = {

    10: 1,
    20: 4,
    30: 5,

}


# ==========================================================
# POLLING LIST
# ==========================================================

POLL_TAGS = [

    TAG_SERIAL_NUMBER,

    TAG_WORKING_MODE,

    TAG_BATTERY_POWER,
    TAG_CHARGING_STATE,
    TAG_BATTERY_SOC,

    TAG_TOTAL_INPUT_POWER,
    TAG_TOTAL_OUTPUT_POWER,

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

]


# ==========================================================
# DOMOTICZ DEVICE DEFINITIONS
# ==========================================================
#
# Domoticz Unit numbers are fixed.
#
# These are the units users will see.
#
# ==========================================================


DEVICE_DEFINITIONS = {


    TAG_SERIAL_NUMBER: {

        "unit": 1,
        "name": "Indevolt Serial Number",
        "type": "text",

    },


    TAG_WORKING_MODE: {

        "unit": 2,
        "name": "Working Mode",
        "type": "selector",

    },


    TAG_CHARGING_STATE: {

        "unit": 3,
        "name": "Charging State",
        "type": "text",

    },


    TAG_BATTERY_POWER: {

        "unit": 4,
        "name": "Battery Power",
        "type": "usage",

    },


    TAG_BATTERY_SOC: {

        "unit": 5,
        "name": "Battery SOC",
        "type": "percentage",

    },


    TAG_TOTAL_INPUT_POWER: {

        "unit": 6,
        "name": "Grid Input Power",
        "type": "usage",

    },


    TAG_TOTAL_OUTPUT_POWER: {

        "unit": 7,
        "name": "Grid Output Power",
        "type": "usage",

    },


    TAG_TOTAL_INPUT_ENERGY: {

        "unit": 8,
        "name": "Total Input Energy",
        "type": "energy",

    },


    TAG_TOTAL_OUTPUT_ENERGY: {

        "unit": 9,
        "name": "Total Output Energy",
        "type": "energy",

    },


    TAG_DAILY_CHARGE: {

        "unit": 10,
        "name": "Battery Daily Charge",
        "type": "custom",
        "unit": "kWh",

    },


    TAG_DAILY_DISCHARGE: {

        "unit": 11,
        "name": "Battery Daily Discharge",
        "type": "custom",
        "unit": "kWh",

    },


    TAG_TOTAL_CHARGE: {

        "unit": 12,
        "name": "Battery Total Charge",
        "type": "custom",
        "unit": "kWh",

    },


    TAG_TOTAL_DISCHARGE: {

        "unit": 13,
        "name": "Battery Total Discharge",
        "type": "custom",
        "unit": "kWh",

    },


    TAG_BACKUP_SOC: {

        "unit": 14,
        "name": "Backup SOC",
        "type": "percentage",

    },


    TAG_RATED_CAPACITY: {

        "unit": 15,
        "name": "Rated Capacity",
        "type": "custom",
        "unit": "kWh",

    },


    TAG_BYPASS_ENABLE: {

        "unit": 16,
        "name": "Bypass Enabled",
        "type": "switch",

    },


    TAG_BYPASS_POWER: {

        "unit": 17,
        "name": "Bypass Power",
        "type": "usage",

    },


    TAG_GRID_VOLTAGE: {

        "unit": 18,
        "name": "Grid Voltage",
        "type": "voltage",

    },


    TAG_GRID_FREQUENCY: {

        "unit": 19,
        "name": "Grid Frequency",
        "type": "custom",
        "unit": "Hz",

    },


    TAG_BATTERY_TEMPERATURE: {

        "unit": 20,
        "name": "Battery Temperature",
        "type": "temperature",

    },

}
