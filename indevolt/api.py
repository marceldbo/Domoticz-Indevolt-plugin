"""
INDEVOLT Domoticz Plugin
Local OpenData API

Version 2.1.0
"""

import json
import urllib.parse

import requests

from .constants import (
    POLL_TAGS,
    SET_WORKING_MODE,
    SET_CHARGING_STATE,
    SET_BYPASS_ENABLE,
    SET_LIGHT_ENABLE,
)

from .helpers import (
    log_debug,
    log_error,
    validate_response,
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
        Read INDEVOLT data.

        Example:

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

            json_config = json.dumps(
                config,
                separators=(
                    ",",
                    ":"
                )
            )

            encoded_config = urllib.parse.quote(
                json_config,
                safe=""
            )

            url = (
                f"{self.base_url}"
                "/rpc/Indevolt.GetData"
                f"?config={encoded_config}"
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
                f"GetData result: {data}"
            )

            if validate_response(data):

                return data

            return {}

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
        Generic SetData command.

        Example:

        {
          "f":16,
          "t":47005,
          "v":[1]
        }

        """

        try:

            if not isinstance(
                values,
                list
            ):

                values = [
                    values
                ]

            config = {

                "f": int(function),

                "t": int(tag),

                "v": values

            }

            json_config = json.dumps(
                config,
                separators=(
                    ",",
                    ":"
                )
            )

            encoded_config = urllib.parse.quote(
                json_config,
                safe=""
            )

            url = (
                f"{self.base_url}"
                "/rpc/Indevolt.SetData"
                f"?config={encoded_config}"
            )

            log_debug(
                f"POST {config}"
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
                f"SetData result: {result}"
            )

            return result

        except Exception as e:


            log_error(
                f"SetData failed: {e}"
            )

            return None

    # ======================================================
    # WORKING MODE COMMAND
    # ======================================================

    def set_working_mode(
        self,
        mode
    ):

        """
        Set INDEVOLT working mode.

        Supported:

        1 = Self-consumed Prioritized
        4 = Real-time Control
        5 = Charge/Discharge Schedule

        """

        return self.set_data(

            function=16,

            tag=SET_WORKING_MODE,

            values=[
                int(mode)
            ]

        )

    # ======================================================
    # CHARGING STATE COMMAND 
    #
    # Note: Only works when WORKING MODE is set to 
    #       Real-time Control.
    # ======================================================

    def set_charging_parameters(
        self,
        state,
        power,
        target_soc
    ):

        """
        Set INDEVOLT charging state.

        Supported:

        0 = Static (Stand-by)
        1 = Charging
        2 = Discharging

        power:

            5-2400 W

        target_soc:

            5-100%

        """

        return self.set_data(

            function=16,

            tag=SET_CHARGING_STATE,

            values=[
                int(state),
                int(power),
                int(target_soc)
            ]

        )
    
    # ======================================================
    # SET BYPASS ENABLE/DISABLE COMMAND
    # ======================================================
        
    def set_bypass(self, enabled):
        """
        Enable or disable Bypass.
    
        True  -> 1
        False -> 0
        """
    
        value = 1 if enabled else 0
    
        return self.set_data(
            function=16,
            tag=SET_BYPASS_ENABLE,
            values=[value]
        )

    # ======================================================
    # SET LIGHT ENABLE/DISABLE COMMAND
    # ======================================================
        
    def set_light(self, enabled):
        """
        Enable or disable Light.
    
        True  -> 1
        False -> 0
        """
    
        value = 1 if enabled else 0
    
        return self.set_data(
            function=16,
            tag=SET_LIGHT_ENABLE,
            values=[value]
        )
