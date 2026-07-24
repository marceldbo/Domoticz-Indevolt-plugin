"""
INDEVOLT Domoticz Plugin
Device handling

Version 2.2.0
"""

import Domoticz

from .constants import (
    DEVICE_DEFINITIONS,
    CHARGING_STATE_LEVELS,
    WORKING_MODE_LEVELS,
)

from .helpers import (
    safe_int,
    safe_float,
    safe_string,
    format_value,
    charging_state,
    charging_state_to_level,
    level_to_charging_state,
    working_mode,
    working_mode_to_level,
    level_to_working_mode,
    log_debug,
    log_error,
)

class DeviceManager:

    def __init__(self, devices, api, config):

        self.Devices = devices
        self.api = api
        self.config = config

        # Current Indevolt working mode
        self.current_working_mode = 1

        # EV override state
        self.rtc_standby_active = False
        
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

                # WORKING MODE Selector needs options
                if tag == 7101:

                    params["Options"] = {

                        "LevelNames":
                            "Self-consumed Prioritized|"
                            "Real-time Control|"
                            "Charge/Discharge Schedule",

                        "LevelActions":
                            "|||",
                        
                        "LevelOffHidden": "True",
                        "SelectorStyle": "1",

                    }

                # CHARGING STATE Selector needs options
                if tag == 6001:

                    params["Options"] = {

                        "LevelNames":
                            "Static (Stand-by)|"
                            "Charging|"
                            "Discharging",

                        "LevelActions":
                            "|||",
                                                
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

    def update_devices(self,data):

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

                    self.current_working_mode = mode
                    
                    mode_level = WORKING_MODE_LEVELS.get(mode, 0)
                    
                    self.Devices[unit].Update(

                    	nValue=1,  # Keeps the switch in active state. No additional 
                                   # "On" action needed after selection change

                        sValue=str(mode_level),
                        
                    )

                    continue

                # ----------------------------------
                # Charging State
                # ----------------------------------
  
                if tag == 6001:

                    state = safe_int(value)

                    state_level = CHARGING_STATE_LEVELS.get(state, 0)

                    self.Devices[unit].Update(

                       nValue=1,  # Keeps the switch in active state. No additional  
                                  # "On" action needed after selection change

                       sValue=str(state_level),

                    )

                    continue

                # ----------------------------------
                # Switches
                # ----------------------------------

                if tag in {680, 7171, 2618}:

                    if tag == 2618:
                        enabled = safe_int(value) == 1001
                    else:
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
    # PROGRAMMATIC CONTROL
    # ======================================================

    def get_working_mode(self):

        return self.current_working_mode

    def set_working_mode(self, mode):

        try:

            result = self.api.set_working_mode(
                mode
            )

            self.current_working_mode = mode

            #
            # Update Domoticz selector immediately
            #

            if 2 in self.Devices:

                level = WORKING_MODE_LEVELS.get(
                    mode,
                    0
                )

                self.Devices[2].Update(

                    nValue=1,

                    sValue=str(level)

                )

            log_debug(
                f"Working Mode set to {mode}: {result}"
            )

            return result

        except Exception as e:

            log_error(
                f"Set Working Mode failed: {e}"
            )

            return None

    def set_rtc_standby(self, enabled):

    try:

        if enabled:

            #
            # Real-time Control standby
            #
            result = self.api.set_charging_parameters(

                state=0,

                power=0,

                target_soc=self.config.discharge_target_soc

            )

            self.rtc_standby_active = True

        else:

            #
            # Exit standby
            #
            result = self.api.set_charging_parameters(

                state=0,

                power=self.config.max_discharge_power,

                target_soc=self.config.discharge_target_soc

            )

            self.rtc_standby_active = False

        log_debug(
            f"RTC Standby {enabled}: {result}"
        )

        return result

    except Exception as e:

        log_error(
            f"RTC Standby failed: {e}"
        )

        return None
    
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

        # Charging state selector
        if unit == 3:
    
            state = level_to_charging_state(level)

            if state == 0:
                
                result = self.api.set_charging_parameters(
            
                    state=0,
        
                    power=0,
        
                    target_soc=self.config.discharge_target_soc
            
                )
            
                log_debug(f"Stand-by enabled: {result}"
                )
            
            elif state == 1:
                
                result = self.api.set_charging_parameters(
                    
                    state=1,
                
                    power=self.config.max_charge_power,
                
                    target_soc=self.config.charge_target_soc
                )
                
                log_debug(f"Charging enabled: {result}"
                )
                    
            elif state == 2:
    
                result = self.api.set_charging_parameters(
    
                    state=2,
    
                    power=self.config.max_discharge_power,
    
                    target_soc=self.config.discharge_target_soc
    
                )
    
                log_debug(f"Discharging enabled: {result}"
                )

            else:
    
                result = self.api.set_charging_parameters(
        
                    state=0,
        
                    power=0,
        
                    target_soc=self.config.discharge_target_soc
        
                )
        
                log_debug(f"Stand-by enabled: {result}"
                )

            return
        
        # Bypass switch
        if unit == 16:
    
            enabled = (command == "On")
    
            result = self.api.set_bypass(enabled)

            #
            # Fake the switch immediately because
            # GetData may not update immediately.
            #
        
            self.Devices[unit].Update(
        
                nValue=1 if enabled else 0,
        
                sValue="On" if enabled else "Off"
        
            )
            
            log_debug(
                f"Bypass {'enabled' if enabled else 'disabled'}: {result}"
            )
    
            return
        
        # Light switch
        if unit == 21:
    
            enabled = (command == "On")
    
            result = self.api.set_light(enabled)

            #
            # Fake the switch immediately because
            # GetData may not update immediately.
            #
        
            self.Devices[unit].Update(
        
                nValue=1 if enabled else 0,
        
                sValue="On" if enabled else "Off"
        
            )
            
            log_debug(
                f"Light {'enabled' if enabled else 'disabled'}: {result}"
            )
    
            return

        # Grid Charging switch
        if unit == 22:
    
            enabled = (command == "On")
    
            result = self.api.set_grid_charging(enabled)

            #
            # Fake the switch immediately because
            # GetData may not update immediately.
            #
        
            self.Devices[unit].Update(
        
                nValue=1 if enabled else 0,
        
                sValue="On" if enabled else "Off"
        
            )
            
            log_debug(
                f"Grid Charging {'enabled' if enabled else 'disabled'}: {result}"
            )
    
            return
