import Domoticz


class DeviceManager:

    DEVICES = {
        1: ("Battery SOC", "Percentage"),
        2: ("Battery Power", "Usage"),
        3: ("Grid Power", "Usage"),
        4: ("PV Power", "Usage"),
        5: ("House Load", "Usage"),
        6: ("Battery Temp", "Temperature"),
        7: ("Battery Voltage", "Voltage"),
        8: ("Battery Current", "Current"),
    }

    def __init__(self, devices_ref):
        # IMPORTANT: Domoticz Devices object passed in
        self.Devices = devices_ref

    def create_devices(self):
        for unit, (name, dtype) in self.DEVICES.items():
            if unit not in self.Devices:
                Domoticz.Device(
                    Name=name,
                    Unit=unit,
                    TypeName=dtype
                ).Create()

    def update_devices(self, data):
        D = self.Devices

        try:
            if 1 in D and "soc" in data:
                D[1].Update(nValue=0, sValue=str(data["soc"]))

            if 2 in D and "battery_power" in data:
                D[2].Update(nValue=0, sValue=str(data["battery_power"]))

            if 3 in D and "grid_power" in data:
                D[3].Update(nValue=0, sValue=str(data["grid_power"]))

            if 4 in D and "pv_power" in data:
                D[4].Update(nValue=0, sValue=str(data["pv_power"]))

            if 5 in D and "load_power" in data:
                D[5].Update(nValue=0, sValue=str(data["load_power"]))

            if 6 in D and "temperature" in data:
                D[6].Update(nValue=0, sValue=str(data["temperature"]))

            if 7 in D and "voltage" in data:
                D[7].Update(nValue=0, sValue=str(data["voltage"]))

            if 8 in D and "current" in data:
                D[8].Update(nValue=0, sValue=str(data["current"]))

        except Exception as e:
            Domoticz.Error(f"Device update error: {e}")
