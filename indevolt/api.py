import requests
import json
import urllib.parse
import Domoticz


class IndevoltAPI:

    def __init__(self, host, username="", password=""):
        self.base_url = f"http://{host}:8080"
        self.session = requests.Session()
        self.auth = (username, password) if username else None

    def _rpc_get(self, tags):
        """
        tags = [1664, 1665, ...]
        """

        config = {
            "t": tags
        }

        encoded = urllib.parse.quote(json.dumps(config))

        url = f"{self.base_url}/rpc/Indevolt.GetData?config={encoded}"

        r = self.session.get(url, auth=self.auth, timeout=10)
        r.raise_for_status()

        return r.json()

    def get_system_data(self):
        """
        Central data fetch using cJSON tags.
        """

        try:
            # 🔥 CORE ENERGY TAG SET (adjustable if needed)
            tags = [
                0,     # Indevolt SN
                7101,  # Indevolt Working Mode
                6000,  # Indevolt Battery Power (W) 
                6001,  # Indevolt Battery Charging State
                6002,  # Indevolt Battery SOC (%)
                2101,  # Indevolt Total Input Power (W)
                2108,  # Indevolt Total Output Power (W)
                2107,  # Indevolt Total Input Energy (kWh)
                2104,  # Indevolt Total Output Energy (kWh)
                6004,  # Indevolt Battery Daily Charge (kWh)
                6005,  # Indevolt Battery Daily Discharge (kWh)
                6006,  # Indevolt Battery Total Charge (kWh)
                6007,  # Indevolt Battery Total Discharge (kWh)
                6105,  # Indevolt Backup SOC (%)
                142,   # Indevolt Rated Capacity (kWh)
                680,   # Indevolt Bypass Mode
                667,   # Indevolt Bypass Power (W)
                2600,  # Indevolt Grid Voltage (V)
                2612,  # Indevolt Grid Fequency (Hz)
                9012,  # Indevolt Battery Temp (C)
                7265,  # Indevolt Light Mode
                47005, # Indevolt Working Mode Setting
                47015, # Indevolt Working Mode State Setting
            ]
            
            data = self._rpc_get(tags)

            return self._normalize(data)

        except Exception as e:
            Domoticz.Error(f"Indevolt RPC error: {e}")
            return {}

    def _normalize(self, raw):
        """
        Convert Indevolt RPC response into flat dict
        """

        result = {}

        try:
            # Expected structure varies slightly by firmware
            # so we defensively parse it

            if isinstance(raw, dict):
                for k, v in raw.items():
                    if isinstance(v, (int, float, str)):
                        result[k] = v

                    elif isinstance(v, dict):
                        # flatten nested
                        for k2, v2 in v.items():
                            result[k2] = v2

        except Exception as e:
            Domoticz.Error(f"Normalization error: {e}")

        return result

    def set_command(self, unit, command, level):
        """
        Optional write support (if Indevolt firmware allows)
        """

        try:
            payload = {
                "unit": unit,
                "command": command,
                "level": level
            }

            self.session.post(
                f"{self.base_url}/rpc/Indevolt.SetControl",
                json=payload,
                auth=self.auth,
                timeout=10
            )

        except Exception as e:
            Domoticz.Error(f"Control error: {e}")
