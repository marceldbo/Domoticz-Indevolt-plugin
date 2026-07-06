import Domoticz
from indevolt.constants import WORKING_MODE_MAP, CHARGING_STATE_MAP, BYPASS_SETTING_MAP, LIGHT_SETTING_MAP

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

        # SWITCHES

        18: ("Bypass Setting", "Switch"),
        19: ("Light", "Switch"),

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

        "7266": 18,
        "7265": 19,
    }
    
    def __init__(self, devices):
        self.Devices = devices

    # -----------------------------
    # CREATE DEVICES
    # -----------------------------
    def create_devices(self):

        for unit, (name, dtype) in self.DEVICES.items():

    #          if unit not in self.Devices:

        if unit == 19:      # Grid Frequency

            Domoticz.Device(
                Name=name,
                Unit=unit,
                Type=243,
                Subtype=31,
                Options={"Custom": "Hz"}
            ).Create()

        else:
            
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
                
               # -----------------------------
                # WORKING MODE (7101)
                # -----------------------------
                if tag == "7101":
                    mode = int(value)
                    text = WORKING_MODE_MAP.get(
                        mode,
                        f"Unknown ({mode})"
                    )

                    self.Devices[unit].Update(
                        nValue=0,
                        sValue=text
                    )
                    continue
                    
                # -----------------------------
                # CHARGING STATE (6001)
                # -----------------------------
                if tag == "6001":
                    raw_state = int(value)
                    state_text = CHARGING_STATE_MAP.get(
                        raw_state,
                        f"Unknown ({raw_state})"
                    )

                    self.Devices[unit].Update(
                        nValue=0,
                        sValue=state_text
                    )
                    continue
                 
                # -----------------------------
                # TEXT DEVICES
                # -----------------------------
                if unit in (1,):
                    self.Devices[unit].Update(0, str(value))
                    continue

                if unit == 2:
                    mode = self._safe_int(value)
                    text = WORKING_MODE_MAP.get(mode, str(mode))
                    self.Devices[unit].Update(0, text)
                    continue

                # -----------------------------
                # SWITCH (Bypass 1: Enable, 0: Disable)
                # -----------------------------
                if unit == 18:
                    state = 1 if int(value) else 0
                    self.Devices[unit].Update(
                        nValue=state,
                        sValue="On" if state else "Off"
                    )
                    continue

                # -----------------------------
                # SWITCH (Light 1: Enable, 0: Disable)
                # -----------------------------
                if unit == 19:
                    state = 1 if int(value) else 0
                    self.Devices[unit].Update(
                        nValue=state,
                        sValue="On" if state else "Off"
                    )
                    continue
               
                # -----------------------------
                # DEFAULT NUMERIC VALUES
                # -----------------------------
                self.Devices[unit].Update(
                    nValue=0,
                    sValue=str(value)
                )

            except Exception as e:
                Domoticz.Error(
                    f"Update error tag {tag} unit {unit}: {e}"
                )
