import requests
import Domoticz


class IndevoltAPI:

    def __init__(self, host, username="", password=""):
        self.base_url = f"http://{host}"
        self.auth = (username, password) if username else None
        self.session = requests.Session()

    def _get(self, path):
        url = f"{self.base_url}{path}"
        r = self.session.get(url, auth=self.auth, timeout=5)
        r.raise_for_status()
        return r.json()

    def get_system_data(self):
        """
        NOTE:
        Endpoint paths are based on Indevolt OpenData concept.
        Adjust if your firmware uses different routes.
        """

        data = {}

        # Core power flow
        try:
            data.update(self._get("/opendata/system"))
        except Exception as e:
            Domoticz.Error(f"System endpoint error: {e}")

        try:
            data.update(self._get("/opendata/battery"))
        except Exception:
            pass

        try:
            data.update(self._get("/opendata/grid"))
        except Exception:
            pass

        try:
            data.update(self._get("/opendata/pv"))
        except Exception:
            pass

        return data

    def set_command(self, unit, command, level):
        """
        Optional control endpoint (may vary per firmware)
        """
        try:
            payload = {
                "unit": unit,
                "command": command,
                "level": level
            }
            self.session.post(
                f"{self.base_url}/opendata/control",
                json=payload,
                auth=self.auth,
                timeout=5
            )
        except Exception as e:
            Domoticz.Error(f"Command failed: {e}")
