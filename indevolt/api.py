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
                1664,  # SOC (example)
                1665,  # Battery Power
                1666,  # Grid Power
                1667,  # PV Power
                1668,  # Load Power
                1669,  # Voltage
                1670,  # Current
                1671   # Temperature
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
