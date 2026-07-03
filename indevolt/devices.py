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

    def create_devices(self):
        for unit, (name, dtype) in self.DEVICES.items():
            if unit not in Devices:
                Domoticz.Device(
                    Name=name,
                    Unit=unit,
                    TypeName=dtype
                ).Create()

    def update_devices(self, data):
        try:
            if 1 in Devices and "soc" in data:
                Devices[1].Update(nValue=0, sValue=str(data["soc"]))

            if 2 in Devices and "battery_power" in data:
                Devices[2].Update(nValue=0, sValue=str(data["battery_power"]))

            if 3 in Devices and "grid_power" in data:
                Devices[3].Update(nValue=0, sValue=str(data["grid_power"]))

            if 4 in Devices and "pv_power" in data:
                Devices[4].Update(nValue=0, sValue=str(data["pv_power"]))

            if 5 in Devices and "load_power" in data:
                Devices[5].Update(nValue=0, sValue=str(data["load_power"]))

            if 6 in Devices and "temperature" in data:
                Devices[6].Update(nValue=0, sValue=str(data["temperature"]))

            if 7 in Devices and "voltage" in data:
                Devices[7].Update(nValue=0, sValue=str(data["voltage"]))

            if 8 in Devices and "current" in data:
                Devices[8].Update(nValue=0, sValue=str(data["current"]))

        except Exception as e:
            Domoticz.Error(f"Device update error: {e}")
