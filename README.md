# Domoticz INDEVOLT Plugin

This plugin for Domoticz uses the local OpenData integration for INDEVOLT home battery systems.

## Feature summary

- Battery SOC monitoring
- Power flow (PV / Grid / Load / Battery)
- Voltage, current, temperature, frequency
- Setting working mode, charging state and bypass
- Automatic device creation
- Local API (no cloud dependency)

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

- The plugin should be selectable under the `Hardware tab`. Look for `Indevolt Battery Monitor`.
- Before configuring, make sure that Domoticz accepts new devices.
- Configure the plugin with a name and ip-address.
- New devices should be visible under Switches, Temperature and Utility and in the `Devices tab`.

For convenience, I have also generated and included an icon to be used with the newly created devices. This can be installed by uploading the `Indevolt stack.zip` file in the custom icons section in the Domoticz GUI and updating the device.
