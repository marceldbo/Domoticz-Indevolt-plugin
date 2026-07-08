"""
INDEVOLT Domoticz Plugin
Local OpenData API communication

Version 2.0.0
"""

import json
import urllib.parse

import requests

from .constants import (
    POLL_TAGS,
    SET_WORKING_MODE,
)

from .helpers import (
    log_debug,
    log_error,
    valid_api_response,
)



class IndevoltAPI:


    def __init__(
        self,
        host,
        port=8080,
        debug=False
    ):

        self.host = host
        self.port = int(port)

        self.base_url = (
            f"http://{self.host}:{self.port}"
        )

        self.timeout = 10

        self.session = requests.Session()


        # Enable debug logging
        from .helpers import set_debug

        set_debug(debug)


        log_debug(
            f"API initialized: {self.base_url}"
        )



    # ======================================================
    # GET DATA
    # ======================================================

    def get_data(self):

        """
        Read all configured INDEVOLT registers.

        Example request:

        /rpc/Indevolt.GetData?
        config={"t":[6000,6001,7101]}

        Returns:

        {
            "6000":0,
            "6001":1000,
            "7101":1
        }

        """

        try:


            config = {

                "t": POLL_TAGS

            }


            encoded = urllib.parse.quote(
                json.dumps(config)
            )


            url = (
                f"{self.base_url}"
                f"/rpc/Indevolt.GetData"
                f"?config={encoded}"
            )


            log_debug(
                f"GET {url}"
            )


            response = self.session.get(
                url,
                timeout=self.timeout
            )


            response.raise_for_status()


            data = response.json()


            log_debug(
                f"GetData response: {data}"
            )


            if not valid_api_response(data):

                return {}


            return data



        except Exception as e:


            log_error(
                f"GetData failed: {e}"
            )


            return {}



    # ======================================================
    # SET DATA
    # ======================================================

    def set_data(
        self,
        function,
        tag,
        values
    ):

        """
        Generic INDEVOLT write command.

        Example:

        {
          "f":16,
          "t":47005,
          "v":[1]
        }

        """


        try:


            if not isinstance(values, list):

                values = [values]


            config = {

                "f": int(function),
                "t": int(tag),
                "v": values

            }


            encoded = urllib.parse.quote(
                json.dumps(config)
            )


            url = (
                f"{self.base_url}"
                f"/rpc/Indevolt.SetData"
                f"?config={encoded}"
            )


            log_debug(
                f"SET {config}"
            )


            response = self.session.post(
                url,
                headers={
                    "Content-Type":
                    "application/json"
                },
                timeout=self.timeout
            )


            response.raise_for_status()


            result = response.json()


            log_debug(
                f"SetData response: {result}"
            )


            return result



        except Exception as e:


            log_error(
                f"SetData failed: {e}"
            )


            return None



    # ======================================================
    # WORKING MODE
    # ======================================================

    def set_working_mode(
        self,
        mode
    ):

        """
        Change INDEVOLT working mode.

        Modes:

        1 = Self-consumed Prioritized
        4 = Real-time Control
        5 = Charge/Discharge Schedule

        """

        return self.set_data(

            function=16,

            tag=SET_WORKING_MODE,

            values=[int(mode)]

        )
