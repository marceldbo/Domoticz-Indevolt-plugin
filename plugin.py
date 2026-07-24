"""
INDEVOLT Domoticz Plugin
Local OpenData API

Domoticz 2026.2
Python 3.11

Version 2.1.0
"""

"""
<plugin key="Indevolt"
        name="Indevolt Home Battery"
        author="Marcel de Bont"
        version="2.1"
        wikilink=""
        externallink="">

    <description>
        Indevolt Home Battery plugin using local OpenData API.
    </description>

    <params>

        <param field="Address"
               label="Indevolt IP"
               width="200px"
               required="true"
               default="192.168.10.142"/>

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
                        value="1"
                        default="false"/>
            </options>
        </param>

    </params>

</plugin>
"""

import Domoticz

from datetime import datetime, timedelta

from indevolt.config import (
    IndevoltConfig
)

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

        self.config = None

        self.interval = 10

        # ==============================
        # EV automation state
        # ==============================

        self.ev_enabled = False

        self.ev_current_device_idx = 0

        self.ev_start_current = 10

        self.ev_stop_current = 2

        self.ev_stop_delay = 10


        self.ev_override_active = False

        self.ev_stop_timer = None

        self.original_working_mode = None

        
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

            self.config = IndevoltConfig()

            self.config.load()

            #
            # EV configuration
            #

            self.ev_enabled = self.config.get(
                "EV_MANAGEMENT_ENABLED",
                False
            )

            self.ev_current_device_idx = int(
                self.config.get(
                    "EV_CURRENT_DEVICE_IDX",
                    0
                )
            )

            self.ev_start_current = float(
                self.config.get(
                    "EV_START_CURRENT",
                    10
                )
            )

            self.ev_stop_current = float(
                self.config.get(
                    "EV_STOP_CURRENT",
                    2
                )
            )

            self.ev_stop_delay = int(
                self.config.get(
                    "EV_STOP_DELAY",
                    10
                )
            )
                
            self.device_manager = DeviceManager(

                Devices,

                self.api,

                self.config

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

            #
            # EV automation
            #

            self.handle_ev_management()
            
        except Exception as e:

            log_error(
                f"Heartbeat failed: {e}"
            )

    # ======================================================
    # EV MANAGEMENT
    # ======================================================

    def get_ev_current(self):

        try:

            device = Domoticz.Device(
                self.ev_current_device_idx
            )

            if device:

                return float(
                    device.sValue
                )

        except Exception as e:

            log_error(
                f"EV current read failed: {e}"
            )

        return None

    def handle_ev_management(self):

        if not self.ev_enabled:

            return

        current = self.get_ev_current()

        if current is None:

            return

        now = datetime.now()

        #
        # EV charging detected
        #

        if current >= self.ev_start_current:

            self.ev_stop_timer = None

            if not self.ev_override_active:

                log_info(
                    f"EV charging detected "
                    f"({current}A)"
                )

                #
                # Save current mode
                #

                self.original_working_mode = (
                    self.device_manager
                    .get_working_mode()
                )

                #
                # Force Real-time Control
                #

                self.device_manager.set_working_mode(
                    4
                )

                #
                # Enable RTC Stand-by
                #

                self.device_manager.set_rtc_standby(
                    True
                )

                self.ev_override_active = True

        #
        # EV stopped
        #

        elif current <= self.ev_stop_current:

            if self.ev_override_active:

                if self.ev_stop_timer is None:

                    self.ev_stop_timer = now

                    log_info(
                        "EV stopped. "
                        "Starting restore timer"
                    )

                elif (
                    now - self.ev_stop_timer
                ) >= timedelta(
                    minutes=self.ev_stop_delay
                ):

                    log_info(
                        "Restoring normal "
                        "battery operation"
                    )

                    self.device_manager.set_rtc_standby(
                        False
                    )

                    self.device_manager.set_working_mode(
                        self.original_working_mode
                        or 1
                    )

                    self.ev_override_active = False

                    self.ev_stop_timer = None
    
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
