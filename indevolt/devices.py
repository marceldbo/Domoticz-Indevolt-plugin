import Domoticz


class DeviceManager:

    # -----------------------------
    # DEVICE DEFINITIONS
    # -----------------------------
    DEVICES = {
        1: ("Indevolt SN", "Text"),
        2: ("Working Mode", "Text"),
        3: ("Battery Power", "Usage"),
        4: ("Charging State", "Text"),
        5: ("Battery SOC", "Percentage"),

        6: ("Total Input Power", "Usage"),
        7: ("Total Output Power", "Usage"),
        8: ("Bypass Power", "Usage"),

        9: ("Grid Voltage", "Voltage"),
        10: ("Grid Frequency", "Custom"),

        11: ("Battery Temperature", "Temperature"),

        # ENERGY COUNTERS (kWh)
        12: ("Energy Input", "kWh"),
        13: ("Energy Output", "kWh"),

        14: ("Daily Charge", "kWh"),
        15: ("Daily Discharge", "kWh"),

        16: ("Total Charge", "kWh"),
        17: ("Total Discharge", "kWh"),
    }

    # -----------------------------
    # TAG MAPPING (cJSON)
    # -----------------------------
    TAG_MAP = {
        "0": 1,
        "7101": 2,

        "6000": 3,
        "6001": 4,
        "6002": 5,

        "2101": 6,
        "2108": 7,
        "667": 8,

        "2600": 9,
        "2612": 10,

        "9012": 11,

        "2107": 12,
        "2104": 13,

        "6004": 14,
        "6005": 15,

        "6006": 16,
        "6007": 17,
    }

    def __init__(self, devices):
        self.Devices = devices

    # -----------------------------
    # CREATE DEVICES
    # -----------------------------
    def create_devices(self):

        for unit, (name, dtype) in self.DEVICES.items():

            if unit not in self.Devices:

                Domoticz.Device(
                    Name=name,
                    Unit=unit,
                    TypeName=dtype
                ).Create()

    # -----------------------------
    # UPDATE DEVICES
    # -----------------------------
    def update_devices(self, data):

        for tag, unit in self.TAG_MAP.items():

            if tag not in data:
                continue

            if unit not in self.Devices:
                continue

            value = data[tag]

            try:

                # TEXT DEVICES
                if unit in (1, 2, 4):
                    self.Devices[unit].Update(
                        nValue=0,
                        sValue=str(value)
                    )

                # ALL NUMERIC (power, energy, voltage, temp)
                else:
                    self.Devices[unit].Update(
                        nValue=0,
                        sValue=str(value)
                    )

            except Exception as e:
                Domoticz.Error(f"Update error tag {tag}: {e}")
