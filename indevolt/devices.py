"""
INDEVOLT Domoticz Plugin - Device Layer
Creates and updates Domoticz devices from API data
"""

import Domoticz

from .constants import DEVICE_DEFINITIONS
from .helpers import (
    safe_int,
    safe_float,
    safe_str,
    format_value,
    mode_to_level,
    log_debug,
    log_error,
)


class DeviceManager:

    def __init__(self, devices, api):
        self.Devices = devices
        self.api = api

    # =========================================================
    # DEVICE CREATION
    # =========================================================

    def create_devices(self):

        for tag, meta in DEVICE_DEFINITIONS.items():

            unit = meta["unit"]
            name = meta["name"]
            dtype = meta["type"]

            if unit in self.Devices:
                continue

            try:

                # -----------------------------
                # SWITCH
                # -----------------------------
                if dtype == "Switch":
                    Domoticz.Device(
                        Name=name,
                        Unit=unit,
                        TypeName="Switch"
                    ).Create()

                # -----------------------------
                # SELECTOR SWITCH (Working Mode)
                # -----------------------------
                elif dtype == "Selector":
                    Domoticz.Device(
                        Name=name,
                        Unit=unit,
                        TypeName="Selector Switch"
                    ).Create()

                # -----------------------------
                # CUSTOM kWh / Hz / kWh-like
                # -----------------------------
                elif dtype == "Custom":
                    Domoticz.Device(
                        Name=name,
                        Unit=unit,
                        Type=243,
                        Subtype=31,
                        Options={"Custom": meta.get("unit_label", "")}
                    ).Create()

                # -----------------------------
                # DEFAULT TYPE NAME DEVICES
                # -----------------------------
                else:
                    Domoticz.Device(
                        Name=name,
                        Unit=unit,
                        TypeName=dtype
                    ).Create()

                log_debug(f"Created device: {name} ({unit})")

            except Exception as e:
                log_error(f"Device creation failed {name}: {e}")

    # =========================================================
    # DEVICE UPDATE
    # =========================================================

    def update_devices(self, data):

        if not isinstance(data, dict):
            log_error("Invalid update data")
            return

        for tag, meta in DEVICE_DEFINITIONS.items():

            unit = meta["unit"]

            if tag not in data:
                continue

            if unit not in self.Devices:
                continue

            value = data[tag]

            try:

                dtype = meta["type"]
                decode = meta.get("decode")

                # -----------------------------
                # SELECTOR (Working Mode)
                # -----------------------------
                if dtype == "Selector":

                    mode = safe_int(value)
                    level = mode_to_level(mode)

                    self.Devices[unit].Update(
                        nValue=0,
                        sValue=str(mode),
                        Level=level
                    )
                    continue

                # -----------------------------
                # SWITCH (Bypass)
                # -----------------------------
                if dtype == "Switch":

                    state = 1 if safe_int(value) else 0

                    self.Devices[unit].Update(
                        nValue=state,
                        sValue="On" if state else "Off"
                    )
                    continue

                # -----------------------------
                # TEXT / DECODED VALUES
                # -----------------------------
                if decode:

                    raw = safe_int(value)
                    text = decode.get(raw, f"Unknown ({raw})")

                    self.Devices[unit].Update(
                        nValue=0,
                        sValue=text
                    )
                    continue

                # -----------------------------
                # CUSTOM (Hz, kWh labels)
                # -----------------------------
                if dtype == "Custom":

                    val = format_value(value)

                    self.Devices[unit].Update(
                        nValue=0,
                        sValue=val
                    )
                    continue

                # -----------------------------
                # DEFAULT NUMERIC
                # -----------------------------
                num = safe_float(value)

                self.Devices[unit].Update(
                    nValue=0,
                    sValue=str(num)
                )

            except Exception as e:
                log_error(f"Update error tag {tag}: {e}")
                
