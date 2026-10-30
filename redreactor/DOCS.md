# Home Assistant App: Red Reactor Battery Monitor

## Installation

Follow these steps to get the app installed on your system:

1. Navigate in your Home Assistant front-end to **Settings** -> **Apps**.
2. Find the "Red Reactor Battery Monitor" app and click it.
3. Click on the "INSTALL" button.

## How to use

The app has a couple of things that must be configured to get the app running as desired:

1. Configure the MQTT settings.
2. Update app settings to suit your needs.
3. Start the app.
4. Check the app log output to see the result.
5. If MQTT Auto Discovery is enabled, the Red Reactor should appear within your Device list

## Configuration

App configuration:

```yaml
mqtt:
  broker: core-mosquitto # IP Address of your MQTT Broker (optional)
  port: 1883 # Port of your MQTT Broker (optional)
  user: redreactor # Username for your MQTT Broker (optional)
  password: redreactor # Password for your MQTT Broker (optional)
  client_id: redreactor-pi # MQTT client ID, must be unique on the broker (optional)
hostname:
  name: redreactor-pi # Hostname (used as a MQTT topic level, so no /, + or #)
  pretty: Raspberry Pi # Pretty Display Name
homeassistant:
  discovery_interval: 120 # Home Assistant Configuration discovery push interval (seconds, 1 or more)
  expire_after: 120 # Home Assistant MQTT Data expiry time (seconds, 0 or more)
system:
  shutdown: ha host shutdown # Shutdown (if using HASS OS, this doesn't need changing)
  restart: ha host restart # Restart (if using HASS OS, this doesn't need changing)
logging:
  console: INFO
  file: WARNING
```

If you use the Mosquitto broker app, leave `broker`, `user` and `password` empty: the app picks up the broker address and credentials from the Supervisor. Anything you set yourself is used instead.

If the broker can't be reached, the app keeps retrying rather than stopping.

Other configuration options are available from within the Home Assistant Device configuration page. Including the ability to change the `report_interval` to Home Assistant.

## OS Specific I2C configuration

_Depending on the operating system you are using, the configuration may differ as below._

### Home Assistant OS

When using the Home Assistant OS, you must enable I2C. This can be enabled by following the steps from within this [Home Assistant guide](https://www.home-assistant.io/common-tasks/os/#enable-i2c).

_The default configuration for this OS is for UART to be disabled - for the Red Reactor to power your Raspberry Pi, it must be enabled. This is due to the Red Reactor requiring UART assertion. It can be found at the same time as configuring the I2C settings, within the `hassos-boot` partition in `config.txt`. Enable it by adding `enable_uart=1` to the `config.txt`_

### Ubuntu

When using a standard operating system, I2C usually comes enabled. Meaning there is no additional configuration to get the Red Reactor working. If it is not enabled it can be done by ensuring the parameter `dtparam=i2c_arm=on` is contained within `/boot/config.txt` file.
