"""
INDEVOLT Domoticz Plugin
Device handling

Version 2.0.0
"""

import Domoticz

from .constants import (
    DEVICE_DEFINITIONS,
    WORKING_MODE_LEVELS,
)

from .helpers import (
    safe_int,
    safe_float,
    safe_string,
    format_value,
    charging_state,
    working_mode,
    working_mode_to_level,
    level_to_working_mode,
    log_debug,
    log_error,
)



class DeviceManager:


    def __init__(
        self,
        devices,
        api
    ):

        self.Devices = devices
        self.api = api



    # ======================================================
    # CREATE DEVICES
    # ======================================================

    def create_devices(self):

        for tag, definition in DEVICE_DEFINITIONS.items():

            unit = definition["unit"]

            if unit in self.Devices:

                continue

            try:

                params = (
                    definition["create"]
                    .copy()
                )

                params["Name"] = (
                    definition["name"]
                )

                params["Unit"] = unit

                # Selector needs options
                if tag == 7101:

                    params["Options"] = {

                        "LevelNames":
                        "Setting|"
                        "Self-consumed Prioritized|"
                        "Real-time Control|"
                        "Charge/Discharge Schedule",

                        "LevelActions":
                        "|10|20|30",
                        
                        "LevelOffHidden": "True",
                        "SelectorStyle": "1",

                    }

                device = Domoticz.Device(
                    **params
                )

                device.Create()

                log_debug(
                    f"Created {definition['name']}"
                )

            except Exception as e:

                log_error(
                    f"Create {definition['name']} failed: {e}"
                )



    # ======================================================
    # UPDATE DEVICES
    # ======================================================

    def update_devices(
        self,
        data
    ):

        if not isinstance(data, dict):

            return

        for tag, definition in DEVICE_DEFINITIONS.items():

            if str(tag) not in data:

                continue

            unit = definition["unit"]


            if unit not in self.Devices:

                continue

            try:


                value = data[str(tag)]

                # ----------------------------------
                # Working Mode
                # ----------------------------------

                if tag == 7101:

                    mode = safe_int(value)

                    level = WORKING_MODE_LEVELS.get(mode, 0)
                    
                    self.Devices[unit].Update(

                        nValue=1,   # Keeps the switch in active state. No additional 
                                    # "On" action needed after selection change

                        sValue=str(level),
                        
                    )

                    continue

                # ----------------------------------
                # Charging State
                # ----------------------------------

                if tag == 6001:

                    state = safe_int(value)

                    self.Devices[unit].Update(

                        nValue=0,

                        sValue=
                        charging_state(
                            state
                        )

                    )

                    continue

                # ----------------------------------
                # Switch
                # ----------------------------------

                if tag == 680:

                    enabled = safe_int(value) == 1

                    self.Devices[unit].Update(

                        nValue=1 if enabled else 0,

                        sValue="On" if enabled else "Off"

                    )

                    continue

                # ----------------------------------
                # Text device
                # ----------------------------------

                if definition["create"].get(
                    "Subtype"
                ) == 19:

                    self.Devices[unit].Update(

                        nValue=0,

                        sValue=
                        safe_string(value)

                    )

                    continue

                # ----------------------------------
                # Numeric devices
                # ----------------------------------

                number = safe_float(
                    value
                )

                self.Devices[unit].Update(

                    nValue=0,

                    sValue=
                    format_value(
                        number
                    )

                )

                log_debug(
                    f"{tag}={number}"
                )

            except Exception as e:

                log_error(
                    f"Update {tag} failed: {e}"
                )

    # ======================================================
    # COMMAND HANDLING
    # ======================================================

    def handle_command(self, unit, command, level):

        # Working Mode selector
        if unit == 2:
    
            mode = level_to_working_mode(level)
    
            if mode is not None:
                result = self.api.set_working_mode(mode)
                log_debug(f"Working Mode changed to {mode}: {result}")
    
            return
    
        # Bypass switch
        if unit == 16:
    
            enabled = (command == "On")
    
            result = self.api.set_bypass(enabled)
    
            log_debug(
                f"Bypass {'enabled' if enabled else 'disabled'}: {result}"
            )
    
            return
