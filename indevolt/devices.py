"""
INDEVOLT Domoticz Plugin
Device management

Version 2.0.0
"""

import Domoticz

from .constants import (
    DEVICE_DEFINITIONS,
    CHARGING_STATE_MAP,
    WORKING_MODE_MAP,
)

from .helpers import (
    safe_int,
    safe_float,
    safe_string,
    format_number,
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


                dtype = definition["type"]


                if dtype == "text":

                    Domoticz.Device(

                        Name=definition["name"],
                        Unit=unit,
                        TypeName="Text"

                    ).Create()



                elif dtype == "selector":


                    Domoticz.Device(

                        Name=definition["name"],
                        Unit=unit,
                        TypeName="Selector Switch",
                        Options={
                            "LevelActions":
                            "||||"
                        }

                    ).Create()



                elif dtype == "switch":


                    Domoticz.Device(

                        Name=definition["name"],
                        Unit=unit,
                        TypeName="Switch"

                    ).Create()



                elif dtype == "percentage":


                    Domoticz.Device(

                        Name=definition["name"],
                        Unit=unit,
                        TypeName="Percentage"

                    ).Create()



                elif dtype == "usage":


                    Domoticz.Device(

                        Name=definition["name"],
                        Unit=unit,
                        TypeName="Usage"

                    ).Create()



                elif dtype == "voltage":


                    Domoticz.Device(

                        Name=definition["name"],
                        Unit=unit,
                        TypeName="Voltage"

                    ).Create()



                elif dtype == "temperature":


                    Domoticz.Device(

                        Name=definition["name"],
                        Unit=unit,
                        TypeName="Temperature"

                    ).Create()



                elif dtype == "energy":


                    Domoticz.Device(

                        Name=definition["name"],
                        Unit=unit,
                        TypeName="Energy"

                    ).Create()



                elif dtype == "custom":


                    Domoticz.Device(

                        Name=definition["name"],
                        Unit=unit,
                        Type=243,
                        Subtype=31,
                        Options={
                            "Custom":
                            definition.get(
                                "unit",
                                ""
                            )
                        }

                    ).Create()



                log_debug(
                    f"Created device {definition['name']}"
                )



            except Exception as e:


                log_error(
                    f"Create device {tag}: {e}"
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


            if tag not in data:

                continue



            unit = definition["unit"]


            if unit not in self.Devices:

                continue



            value = data[tag]


            try:


                dtype = definition["type"]



                # ----------------------------------
                # Working mode selector
                # ----------------------------------

                if tag == "7101":


                    mode = safe_int(value)


                    self.Devices[unit].Update(

                        nValue=0,

                        sValue=
                        WORKING_MODE_MAP.get(
                            mode,
                            "Unknown"
                        ),

                        Level=
                        working_mode_to_level(
                            mode
                        )

                    )


                    continue



                # ----------------------------------
                # Charging state text
                # ----------------------------------

                if tag == "6001":


                    state = safe_int(value)


                    self.Devices[unit].Update(

                        nValue=0,

                        sValue=
                        CHARGING_STATE_MAP.get(
                            state,
                            f"Unknown ({state})"
                        )

                    )


                    continue



                # ----------------------------------
                # Switch
                # ----------------------------------

                if dtype == "switch":


                    state = 1 if safe_int(value) else 0


                    self.Devices[unit].Update(

                        nValue=state,

                        sValue=
                        "On" if state else "Off"

                    )


                    continue



                # ----------------------------------
                # Numeric devices
                # ----------------------------------

                self.Devices[unit].Update(

                    nValue=0,

                    sValue=
                    format_number(
                        safe_float(value)
                    )

                )



            except Exception as e:


                log_error(
                    f"Update {tag}: {e}"
                )



    # ======================================================
    # DOMOTICZ COMMANDS
    # ======================================================

    def handle_command(
        self,
        unit,
        command,
        level
    ):


        # Working Mode selector

        if unit != 2:

            return



        mode = level_to_working_mode(
            level
        )


        if mode is None:

            return



        result = self.api.set_working_mode(
            mode
        )


        log_debug(
            f"Working mode changed: {result}"
        )
