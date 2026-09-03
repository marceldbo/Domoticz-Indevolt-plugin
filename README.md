# Domoticz INDEVOLT Plugin

This plugin for Domoticz uses the local OpenData API for INDEVOLT home battery systems.

## Implemented features summary

- Battery SOC monitoring
- Power flow (Grid / Load / Battery)
- Domoticz Energy Dashboard support with correct battery flow direction
- Setting of Working mode, Charging state, Grid charging and Bypass socket
- Automatic device creation: power, SOC, charging, discharging, voltage, current, temperature, frequency etc.
- Automatic device creation for battery statistics e.g. Round-trip Efficiency (RTE), Throughput and Cycles
- Uses local Indevolt OpenData API (no cloud dependency)
- Optional EV-management with automatic EV-Current sensing device creation

## Installation

To install:

- Go into the Domoticz plugins directory using a command line.
- Run: `git clone https://github.com/marceldbo/Domoticz-Indevolt-plugin.git`
- Run: `python3 -m pip install -r requirements.txt` or if running a python virtual environment, copy the requirements.txt file into the activated venv and run `pip install -r requirements.txt`
- Restart Domoticz

To update:

- From the Domoticz plugins directory, using a command line, go into the Domoticz-Indevolt-plugin directory.
- Run: `git pull`
- Restart Domoticz

## Configuration

- The plugin should be selectable under the `Hardware tab`. Look for `Indevolt Home Battery`.
- Before configuring, make sure that Domoticz accepts new devices.
- Configure the plugin with a name and ip-address.
- New devices should be visible under Switches, Temperature and Utility and in the `Devices tab`. I have selected the most used devices to be visible immediately as real devices in the dashboard. Under the 'Devices tab', there are more selectable devices e.g. Grid Voltage, Grid Frequency etc.
- Under the 'User variables' tab as part of 'More options', the desired values for Charging, Discharging and Desired State-of-Charge, can be changed in case you don't like the default values. Check the regulations for your country regarding allowable (and safe) values! In the Netherlands, the maximum charging power is 2400 W. The maximum discharge power depends on the electrical installation: 800 W when using a standard wall socket, and 2400 W when connected to a dedicated and protected circuit in the electrical distribution unit. After updating the values, stop and start the plugin from the Domoticz Hardware tab.

## Electric Vehicle (EV) Management

If you have an EV and want to prevent your home battery from discharging while your vehicle is charging, you can enable **EV Management**. When enabled, the battery is automatically forced into **Static (Stand-by)** mode whenever the measured EV charging current exceeds a configurable threshold. The battery remains in this state for as long as the charging current stays above that threshold.

To enable this feature, go to **User Variables** and set **EV Management** to **1** (enabled). You can also configure the following parameters:

* **Start threshold (A):** The charging current above which EV Management is activated (min: 1A, max: 10A).
* **Stop threshold (A):** The charging current below which EV Management is deactivated (min: 1A, max: 5A).
* **Stop delay (minutes):** The amount of time the charging current must remain below the stop threshold before EV Management is disabled (min: 1 min, max: 120 mins).

The stop delay prevents rapid switching when EV charging is briefly interrupted, for example during communication between the charger and the vehicle. Another use case is when you charge your EV during a partly cloudy day. Once the configured delay has elapsed, the battery automatically returns to the operating mode it was in before EV charging started. After updating the values, stop and start the plugin from the Domoticz Hardware tab.

The charging current can be measured using a Zigbee energy monitor with a current transformer (CT). Install the CT around one of the charging station's supply conductors and integrate the sensor with **Zigbee2MQTT**. Use **Node-RED** to forward the measured current (in amperes) to the Domoticz **EV Current** sensor used by the plugin.

For testing purposes, you can also use Node-RED to inject a simulated current value into the EV Current sensor, allowing you to verify the EV Management functionality without connecting an actual EV charger.

## Icon

For convenience, I have generated and included an icon to be used with the newly created devices. This can be installed by uploading the `Indevolt stack.zip` file in the custom icons section in the Domoticz GUI and updating the device.

## Ideas and TO DO's

- More generic external controls e.g. external control for a Heat Exchanger, etc.
- Support for separate language files as currently the devices are created in English.
- Adding a combined text device with system serial numbers, RTE, charge/discharge cycles etc.  
