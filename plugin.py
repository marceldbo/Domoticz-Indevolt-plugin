"""
INDEVOLT Domoticz Plugin
Local OpenData API

Domoticz 2026.2
Python 3.11

Version 2.0.0
"""

"""
<plugin key="Indevolt"
        name="Indevolt Home Battery"
        author="Marcel de Bont"
        version="2.0.0"
        wikilink=""
        externallink="">

    <description>
        Indevolt Home Battery plugin using local OpenData API.
    </description>

    <params>

        <param field="Address"
               label="Indevolt IP"
               width="200px"
               required="true"/>

        <param field="Port"
               label="Port"
               width="60px"
               required="false"
               default="8080"/>

        <param field="Mode1"
               label="Update Interval (sec)"
               width="75px"
               required="false"
               default="10"/>

        <param field="Mode6"
               label="Debug logging"
               width="75px"
               required="false">
            <options>
                <option label="Off"
                        value="0"
                        default="true"/>
                <option label="On"
                        value="1"/>
            </options>
        </param>

    </params>

</plugin>
"""

import Domoticz

from indevolt.api import (
    IndevoltAPI
)

from indevolt.devices import (
    DeviceManager
)

from indevolt.helpers import (
    log_error,
    log_info,
)

class BasePlugin:

    def __init__(self):

        self.api = None

        self.device_manager = None

        self.interval = 10

    # ======================================================
    # START
    # ======================================================

    def onStart(self):

        try:

            log_info(
                "Starting INDEVOLT plugin"
            )

            host = Parameters["Address"]

            port = int(
                Parameters.get(
                    "Port",
                    8080
                )
            )

            self.interval = int(
                Parameters.get(
                    "Mode1",
                    10
                )
            )

            debug = (

                Parameters.get(
                    "Mode6",
                    "0"
                )

                == "1"

            )

            self.api = IndevoltAPI(

                host,

                port,

                debug

            )

            self.device_manager = DeviceManager(

                Devices,

                self.api

            )

            self.device_manager.create_devices()

            Domoticz.Heartbeat(

                self.interval

            )

            log_info(
                "INDEVOLT plugin started"
            )

        except Exception as e:

            log_error(
                f"Startup failed: {e}"
            )

    # ======================================================
    # STOP
    # ======================================================

    def onStop(self):

        log_info(
            "INDEVOLT plugin stopped"
        )

    # ======================================================
    # HEARTBEAT
    # ======================================================

    def onHeartbeat(self):

        try:

                data = (
                self.api
                .get_data()
            )


            if data:

                self.device_manager.update_devices(
                    data
                )

        except Exception as e:

            log_error(
                f"Heartbeat failed: {e}"
            )

    # ======================================================
    # COMMANDS
    # ======================================================

    def onCommand(
        self,
        Unit,
        Command,
        Level,
        Hue
    ):

        try:

            self.device_manager.handle_command(

                Unit,

                Command,

                Level

            )

        except Exception as e:

            log_error(
                f"Command failed: {e}"
            )

# ==========================================================
# DOMOTICZ ENTRY POINTS
# ==========================================================

global _plugin

_plugin = BasePlugin()

def onStart():

    _plugin.onStart()

def onStop():

    _plugin.onStop()

def onHeartbeat():

    _plugin.onHeartbeat()

def onCommand(
    Unit,
    Command,
    Level,
    Hue
):

    _plugin.onCommand(
        Unit,
        Command,
        Level,
        Hue
    )
