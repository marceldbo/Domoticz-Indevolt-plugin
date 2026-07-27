# Domoticz INDEVOLT Plugin

This plugin for Domoticz uses the local OpenData integration for INDEVOLT home battery systems.

## Implemented features summary

- Battery SOC monitoring
- Power flow (Grid / Load / Battery)
- Voltage, current, temperature, frequency
- Setting of Working mode, Charging state, Grid charging and Bypass socket
- Automatic device creation
- Local API (no cloud dependency)
- Automatic EV-Current sensing device creation

## Installation

To install:

- Go into the Domoticz plugins directory using a command line.
- Run: `git clone https://github.com/marceldbo/Domoticz-Indevolt-plugin.git`
- Restart Domoticz.

To update:

- From the Domoticz plugins directory, using a command line, go into the Domoticz-Indevolt-plugin directory.
- Run: `git pull`
- Restart Domoticz.

## Configuration and additional notes

- The plugin should be selectable under the `Hardware tab`. Look for `Indevolt Home Battery`.
- Before configuring, make sure that Domoticz accepts new devices.
- Configure the plugin with a name and ip-address.
- New devices should be visible under Switches, Temperature and Utility and in the `Devices tab`. I have selected the most used devices to be visible immediately as real devices in the dashboard. Under the 'Devices tab', there are more selectable devices e.g. Grid Voltage, Grid Frequency etc.
- Under the 'User variables' tab as part of 'More options', the desired values for Charging, Discharging and Desired State-of-Charge, can be changed in case you don't like the default values. Check the regulations for your country regarding allowable (and safe) values! In the Netherlands, the maximum charging power is 2400 W. The maximum discharge power depends on the electrical installation: 800 W when using a standard wall socket, and 2400 W when connected to a dedicated and protected circuit in the electrical distribution unit.
- If you have an EV, and you don't want the battery discharging while charging your EV, you can enable EV-management. The battery will be forced into 'Static (Stand-by)' for as long as the EV charging currunt is above a set threshold. To enable this feature, go to 'User variables' and set the value to '1'. You can set the desired values for the start/stop threshold currents (Amps) and the stop-delay (Minutes). The latter is used to overcome rapid state changes when charging stops momentarily. After the configured stop-delay time, the battery returns to the state it was in, before the EV charging started. The actual current sensing device can be a Zigbee Energy Monitor with a Current Transformer (pick your preferred online warehouse) and place the "CT" over one of the Charging Station feeds. Use Zigbee2mqtt and Node-RED to send the current value in Amps to the Domoticz EV-Current sensing device. To test, you can also create a dummy feed into the sensor using Node-RED.

For convenience, I have generated and included an icon to be used with the newly created devices. This can be installed by uploading the `Indevolt stack.zip` file in the custom icons section in the Domoticz GUI and updating the device.
