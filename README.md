# p3exporter collector module for FritzBox smarthome data

[![PyPI version](https://badge.fury.io/py/p3exporter-fritzbox-smarthome.svg)](https://badge.fury.io/py/p3exporter-fritzbox-smarthome)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/56c57d4c4dbb440a944a8fbd5f5533a8)](https://www.codacy.com/gh/codeaffen/p3exporter-fritzbox-smarthome/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=codeaffen/p3exporter-fritzbox-smarthome&amp;utm_campaign=Badge_Grade)

This module provides collector for FritzBox smarthome device data. It can be enabled with a default p3exporter installation via `p3.yml`.

The collector is in a very early state and it provides temperature data from connected thermostat devices with temperature sensors.

Tested with:

* Comet DECT thermostat

## Installation and Running

You need to install `p3exporter` first. It is available on [pypi](https://pypi.org/project/p3exporter/) so you can use `pip` to install the exporter and run it locally.

```shell
pip install p3exporter
```

Now you need to install `p3exporter-fritzbox-smarthome`. Choose one method mentioned below.

### Install from pypi.org

We also provide a pypi.org package. You can install the collector with the following command:

```shell
pip install p3exporter-fritzbox-smarthome
```

### Install from repository

You can install it from a local clone of our [github repository](https://github.com/codeaffen/p3exporter-fritzbox-smarthome).

```shell
$ git clone https://github.com/codeaffen/p3exporter-fritzbox-smarthome.git
Cloning into 'p3exporter-fritzbox-smarthome'...
...
$ cd p3exporter-fritzbox-smarthome
$ pip install -e .
```

## Activation FritzBox smarthome collectors

To start `p3exporter` you need a valid `p3.yml` you can either edit an existing one or take the example from this repository.

```shell
curl --silent https://raw.githubusercontent.com/codeaffen/p3exporter-fritzbox-smarthome/develop/p3.yml.example --output ~/tmp/p3.yml
```

If you edit an existing `p3.yml` add the following content to activate the collector.

```yaml
exporter_name: "Python prammable Prometheus exporter /w FritzBox collector"
collectors:
  - p3eFritzBox.collector.smarthome
collector_opts:
  smarthome:
    defaults:
      hostname: https://fb.example.com # use this hostname as default (if never set hostname defaults to 'https://fritz.box')
      username: smarthome # use this username as default
      ssl_verify: false # disable ssl certificate verification by default
    devices:
      - name: FB@home
        password: v3rys3cr3t
      - name: FB@cottage
        password: 4l5ov3rys3cr3t
        hostname: https://myfritzbox.example.com
        ssl_verify: true # enable ssl certificate verification for this device connection
```

After that you can start the p3exporter as usual:

```shell
$ p3exporter -c /tmp/p3.yml
INFO:root:Collector 'p3eFritzBox.collector.smarthome' was loaded and registred successfully
INFO:root:Start exporter, listen on 5876
```

## Configuration

To configure this collector you need to create a dict with the connection parameters within the `devices` list.
There are some parameters avaiable to configure the collector. In the following table all parameters are listed.

<!-- markdownlint-disable MD033 MD034 -->
Name | Default | Mandatory | Description
--- | --- | --- | ---
name  | | device_\<NUM\> | An arbitrary name to identify metrics according the device. If not given it will be generated as seen in default column. `<NUM>` stands for the list index, starting with 1.
username |  | * | Username used to authenticate against FritzBox
password |  | * | Password used to authenticate against FritzBox
hostname | https://fritz.box | | Hostname of FritzBox to connect to. Protocol can be `http` or `https`. If no protocol is given default will be `https`.
device_types | | | List of device type to enable. If List is empty all device types are activated. Possible values are:<br/><ul><li>temperature_sensor</li></ul>
ssl_verify | True | | Set to `True` to disable ssl certificate verfication. This is useful in case of using self signed certificates.<br/>**Note**: To use this parameter `pyfritzhome` from github is needed as the ssl_verify parameter is not yet available in pypi package. For details use `requirements.txt`.
<!-- markdownlint-enable MD033 MD034 -->

All parameters from the table above except `name` can also be defined in `defaults` dict. Parameters defined here will be used as defaults for each device in devices list if the corresponding parameter is not defined there.
