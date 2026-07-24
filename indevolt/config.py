"""
INDEVOLT Domoticz Plugin
Configuration Manager

Version 2.2.0
"""

import requests

from .helpers import (
    log_debug,
    log_error,
)

# ======================================================
# DEFAULT BATTERY SETTINGS
# ======================================================

DEFAULT_SETTINGS = {

    "Indevolt_ChargeTargetSOC": {
        "default": 100,
        "min": 5,
        "max": 100,
    },

    "Indevolt_DischargeTargetSOC": {
        "default": 20,
        "min": 5,
        "max": 100,
    },

    "Indevolt_MaxChargePower": {
        "default": 2400,
        "min": 50,
        "max": 2400,
    },

    "Indevolt_MaxDischargePower": {
        "default": 800,
        "min": 50,
        "max": 2400,
    },

}

# ======================================================
# DEFAULT EV MANAGEMENT SETTINGS
# ======================================================

DEFAULT_EV_SETTINGS = {

    "Indevolt_EV_Management_Enabled": {
        "default": 0,
        "min": 0,
        "max": 1,
    },

    "Indevolt_EV_Current_Device_IDX": {
        "default": 0,
        "min": 0,
        "max": 99999,
    },

    "Indevolt_EV_Start_Current": {
        "default": 3,
        "min": 1,
        "max": 5,
    },

    "Indevolt_EV_Stop_Current": {
        "default": 2,
        "min": 0,
        "max": 5,
    },

    "Indevolt_EV_Stop_Delay": {
        "default": 10,
        "min": 5,
        "max": 120,
    },

}

# ======================================================
# CONFIGURATION CLASS
# ======================================================

class IndevoltConfig:

    def __init__(
        self,
        host="127.0.0.1",
        port=8080
    ):

        self.base_url = (
            f"http://{host}:{port}/json.htm"
        )

        # Cached values

        self.charge_target_soc = 100
        self.discharge_target_soc = 20

        self.max_charge_power = 2400
        self.max_discharge_power = 2400

        # Cached EV values

        self.ev_management_enabled = False
        self.ev_current_device_idx = 0
        self.ev_start_current = 3
        self.ev_stop_current = 2
        self.ev_stop_delay = 10

    # ==================================================
    # READ USER VARIABLES
    # ==================================================

    def get_variables(self):

        try:

            url = (
                self.base_url
                + "?type=command"
                + "&param=getuservariables"
            )

            result = requests.get(
                url,
                timeout=5
            ).json()

            variables = {}

            for item in result.get(
                "result",
                []
            ):

                variables[item["Name"]] = (
                    item["Value"]
                )

            return variables

        except Exception as e:

            log_error(
                f"Read user variables failed: {e}"
            )

            return {}

    # ==================================================
    # CREATE VARIABLE
    # ==================================================

    def create_variable(
        self,
        name,
        value
    ):

        try:

            url = (
                self.base_url
                + "?type=command"
                + "&param=adduservariable"
                + f"&vname={name}"
                + "&vtype=0"
                + f"&vvalue={value}"
            )

            requests.get(
                url,
                timeout=5
            )

            log_debug(
                f"Created variable {name}={value}"
            )

        except Exception as e:

            log_error(
                f"Create {name} failed: {e}"
            )

    # ==================================================
    # UPDATE CACHE
    # ==================================================

    def load(self):

        variables = self.get_variables()

        for name, cfg in DEFAULT_SETTINGS.items():

            if name not in variables:

                self.create_variable(
                    name,
                    cfg["default"]
                )

                value = cfg["default"]

            else:

                value = int(
                    variables[name]
                )

            # Validate

            value = max(
                cfg["min"],
                value
            )

            value = min(
                cfg["max"],
                value
            )

            # Store internally

            if name == "Indevolt_ChargeTargetSOC":

                self.charge_target_soc = value

            elif name == "Indevolt_DischargeTargetSOC":

                self.discharge_target_soc = value

            elif name == "Indevolt_MaxChargePower":

                self.max_charge_power = value

            elif name == "Indevolt_MaxDischargePower":

                self.max_discharge_power = value

        log_debug(
            "Indevolt configuration loaded"
        )

    # ==================================================
    # REFRESH
    # ==================================================

    def refresh(self):

        self.load()
