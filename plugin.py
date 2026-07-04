"""
INDEVOLT Domoticz Plugin (Local OpenData API)
Tested for Domoticz 2026.2 (Python 3.11)
Author: Marcel de Bont / OpenAI
"""
"""
<plugin key="Indevolt" name="Indevolt Home Battery" author="Marcel de Bont" version="1.0.0" wikilink="" externallink="https://github.com/marceldbo/Domoticz-Indevolt-Plugin.git">
    <description>
        Indevolt Home Battery plugin for Domoticz.
    </description>
    <params>
        <param field="Address" label="Indevolt IP" width="200px" required="true"/>
        <param field="Mode1" label="Update Interval (sec)" width="75px" required="false" default="10"/>
    </params>
</plugin>
"""

import Domoticz
from indevolt.api import IndevoltAPI
from indevolt.devices import DeviceManager

class BasePlugin:

    def __init__(self):
        self.api = None
        self.device_manager = None

    def onStart(self):
        Domoticz.Log("INDEVOLT plugin starting...")

        self.ip = Parameters["Address"]
        self.username = Parameters.get("Username", "")
        self.password = Parameters.get("Password", "")
        self.poll = int(Parameters.get("Mode1", 10))

        self.api = IndevoltAPI(self.ip, self.username, self.password)
        self.device_manager = DeviceManager(Devices)

        Domoticz.Heartbeat(self.poll)

        # Create devices
        self.device_manager.create_devices()

        Domoticz.Log("INDEVOLT plugin started.")

    def onStop(self):
        Domoticz.Log("INDEVOLT plugin stopped.")

    def onHeartbeat(self):
        try:
            data = self.api.get_system_data()
            self.device_manager.update_devices(data)
        except Exception as e:
            Domoticz.Error(f"Heartbeat error: {e}")

    def onCommand(self, Unit, Command, Level, Color):
        Domoticz.Log(f"Command received: {Unit} -> {Command}")
        self.api.set_command(Unit, Command, Level)


global _plugin
_plugin = BasePlugin()

def onStart():
    _plugin.onStart()

def onStop():
    _plugin.onStop()

def onHeartbeat():
    _plugin.onHeartbeat()

def onCommand(Unit, Command, Level, Color):
    _plugin.onCommand(Unit, Command, Level, Color)
