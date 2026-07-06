"""
INDEVOLT Domoticz Plugin - API Layer
Handles GetData + SetData RPC communication
"""

import json
import urllib.parse
import requests
import Domoticz

from .helpers import log_debug, log_error


class IndevoltAPI:

    def __init__(self, host, port=8080, timeout=10):
        self.host = host
        self.port = port
        self.timeout = timeout

        self.base_url = f"http://{host}:{port}"
        self.session = requests.Session()

    # =========================================================
    # GET DATA (polling)
    # =========================================================

    def get_data(self, tags):
        """
        tags: list of INDEVOLT register IDs
        returns: dict
        """

        try:
            payload = {
                "t": tags
            }

            url = (
                f"{self.base_url}/rpc/Indevolt.GetData"
                f"?config={urllib.parse.quote(json.dumps(payload))}"
            )

            r = self.session.get(url, timeout=self.timeout)

            if r.status_code != 200:
                log_error(f"GetData HTTP {r.status_code}")
                return {}

            data = r.json()

            if not isinstance(data, dict):
                log_error(f"Invalid GetData response: {data}")
                return {}

            return data

        except Exception as e:
            log_error(f"GetData exception: {e}")
            return {}

    # =========================================================
    # SET DATA (control / write)
    # =========================================================

    def set_data(self, f, t, v):
        """
        Generic INDEVOLT write command

        f = function code (e.g. 16 write)
        t = register id
        v = list of values
        """

        try:
            payload = {
                "f": int(f),
                "t": int(t),
                "v": v if isinstance(v, list) else [v]
            }

            url = f"{self.base_url}/rpc/Indevolt.SetData"

            full_url = url + "?config=" + urllib.parse.quote(json.dumps(payload))

            r = self.session.post(full_url, timeout=self.timeout)

            if r.status_code != 200:
                log_error(f"SetData HTTP {r.status_code}: {r.text}")
                return False

            log_debug(f"SetData OK: {payload}")
            return True

        except Exception as e:
            log_error(f"SetData exception: {e}")
            return False

    # =========================================================
    # CONVENIENCE METHOD: WORKING MODE
    # =========================================================

    def set_working_mode(self, mode):
        """
        mode:
            1 = Self-consumed Prioritized
            4 = Real-time Control
            5 = Charge/Discharge Schedule
        """

        return self.set_data(
            f=16,
            t=47005,
            v=[int(mode)]
        )
