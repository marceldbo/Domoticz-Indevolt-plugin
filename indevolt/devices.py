import Domoticz
from indevolt.constants import WORKING_MODE_MAP, CHARGING_STATE_MAP, BYPASS_MODE_SETTING_MAP, LIGHT_MODE_SETTING_MAP, WORKING_MODE_SETTING_MAP, WORKING_MODE_STATE_SETTING_MAP

class DeviceManager:

    # -----------------------------
    # DEVICE DEFINITIONS
    # -----------------------------
    DEVICES = {
        1: ("Serial Number", "Text"),
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
        20: ("Energy Input", "kWh"),
        21: ("Energy Output", "kWh"),

        22: ("Daily Charge", "kWh"),
        23: ("Daily Discharge", "kWh"),

        24: ("Total Charge", "kWh"),
        25: ("Total Discharge", "kWh"),

        # SWITCHES
        30: ("Bypass Mode Setting", "Switch"),
        31: ("Light Mode Setting", "Switch"),
       
        32: ("Working Mode Setting", "Switch"),
        33: ("Working Mode State Setting", "Switch"),

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

        "2107": 20,
        "2104": 21,

        "6004": 22,
        "6005": 23,

        "6006": 24,
        "6007": 25,

        "7266": 30,
        "7265": 31,

        "47005": 32,
        "47015": 33,
    }
    
    def __init__(self, devices):
        self.Devices = devices

    # -----------------------------
    # CREATE DEVICES
    # -----------------------------
    def create_devices(self):

        for unit, (name, dtype) in self.DEVICES.items():

    #          if unit not in self.Devices:

            if unit == 10:      # Grid Frequency

                Domoticz.Device(
                    Name=name,
                    Unit=unit,
                    Type=243,
                    Subtype=31,
                    Options={'Custom': '1;Hz'}
                ).Create()

                continue

            if unit in (20, 21, 22, 23, 24, 25):      # kWh custom sensors

                Domoticz.Device(
                    Name=name,
                    Unit=unit,
                    Type=243,
                    Subtype=31,
                    Options={'Custom': '1;kWh'}
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
                # SWITCH (Bypass 1: Enable (On), 0: Disable (Off))
                # -----------------------------
                if unit == 30:
                    state = 1 if int(value) else 0
                    self.Devices[unit].Update(
                        nValue=state,
                        sValue="On" if state else "Off"
                    )
                    continue

                # -----------------------------
                # SWITCH (Light 1: Enable (On), 0: Disable (Off))
                # -----------------------------
                if unit == 31:
                    state = 1 if int(value) else 0
                    self.Devices[unit].Update(
                        nValue=state,
                        sValue="On" if state else "Off"
                    )
                    continue

                # -----------------------------
                # SWITCH Working Mode Setting
                #  
                #   1: Self-consumed Prioritized, 
                #   4: Real-time control
                #   5: Charge/Discharge Schedule (Not implemented)
                #
                # -----------------------------
                if unit == 32:
                    state = 4 if int(value) else 1
                    self.Devices[unit].Update(
                        nValue=state,
                        sValue="Real-time control" if state else "Self-consumed Prioritized"
                    )
                    continue

                # -----------------------------
                # SWITCH Working Mode State Setting 
                #
                #    0: Standby, 
                #    1: Charging,
                #    2: Discharging
                # 
                # -----------------------------
                if unit == 33:
                    state = 1 if int(value) else 0
                    self.Devices[unit].Update(
                        nValue=state,
                        sValue="Charging" if state else "Standby"
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
