# p3exporter collector module for FritzBox smarthome data

[![PyPI version](https://badge.fury.io/py/p3exporter-fritzbox-smarthome.svg)](https://badge.fury.io/py/p3exporter-fritzbox-smarthome)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/56c57d4c4dbb440a944a8fbd5f5533a8)](https://www.codacy.com/gh/codeaffen/p3exporter-fritzbox-smarthome/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=codeaffen/p3exporter-fritzbox-smarthome&amp;utm_campaign=Badge_Grade)

This module provides collector for FritzBox smarthome device data. It can be enabled with a default p3exporter installation via `p3.yml`.

The collector is in a very early state and it provides temperature data from connected thermostat devices with temperature sensors.

Tested with:

* Comet DECT thermostat

## Installation and Running

You need to install `p3exporter` first. It is available on [pypi](https://pypi.org/project/p3exporter/) so you can use `pip` to install the exporter and run it locally.

```text
pip install p3exporter
```

Now you need to install `p3exporter-fritzbox-smarthome`. Choose one method mentioned below.

### Install from pypi.org

***Not yet available***

### Install from repository

You can install it from a local clone of our [github repository](https://github.com/codeaffen/p3exporter-fritzbox-smarthome).

```text
$ git clone https://github.com/codeaffen/p3exporter-fritzbox-smarthome.git
Cloning into 'p3exporter-fritzbox-smarthome'...
...
$ cd p3exporter-fritzbox-smarthome
$ pip install -e .
```

## Activation FritzBox smarthome collectors

To start `p3exporter` you need a valid `p3.yml` you can either edit an existing one or take the example from this repository.

```shell
cp p3.yml.example /tmp/p3.yml
```

If you edit an existing `p3.yml` add the following content to activate the collector.

```yaml
collectors:
  - p3eFritzBox.collector.smarthome
collector_opts:
  smarthome:
    username: smarthome
    password: v3rys3cr3t
```

After that you can start the p3exporter as usual:

```shell
$ p3exporter -c /tmp/p3.yml
INFO:root:Collector 'p3eFritzBox.collector.smarthome' was loaded and registred successfully
INFO:root:Start exporter, listen on 5876
```

## Configuration

There are some parameters avaiable to configure the collector. In the following table all parameters are listed.

<!-- markdownlint-disable MD033 MD034 -->
Name | Default | Mandatory | Description
--- | --- | --- | ---
username |  | * | Username used to authenticate against FritzBox
password |  | * | Password used to authenticate against FritzBox
hostname | https://fritz.box | | Hostname of FritzBox to connect to. Protocol can be `http` or `https`. If no protocol is given default will be `https`.
device_types | | | List of device type to enable. If List is empty all device types are activated. Possible values are:<br/><ul><li>temperature_sensor</li></ul>
ssl_verify | False | | Set to `True` to disable ssl certificate verfication. This is useful in case of using self signed certificates.<br/>**Note**: To use this parameter `pyfritzhome` from github is needed as the ssl_verify parameter is not yet available in pypi package. For details use `requirements.txt`.
<!-- markdownlint-enable MD033 MD034 -->

