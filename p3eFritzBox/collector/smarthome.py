"""Module that defines all needed classes and functions for example collector."""
import logging

from p3exporter.collector import CollectorBase, CollectorConfig
from prometheus_client.core import GaugeMetricFamily, InfoMetricFamily

from pyfritzhome import Fritzhome, LoginError


class SmarthomeCollector(CollectorBase):
    """A sample collector.

    It does not really do much. It only runs a method and return the time it runs as a gauge metric.
    """

    def __init__(self, config: CollectorConfig):
        """Instanciate a MyCollector object."""
        super(SmarthomeCollector, self).__init__(config)

        # Define connection defaults in a dictionary
        # Combine connection with user defined defautls
        self._connection_defaults = dict(username=None, password=None, hostname="https://fritz.box", ssl_verify=True, device_types=[])
        self.defaults = {**self._connection_defaults, **self.opts.pop("defaults", {})}
        self.devices = []

        # Create device dictionary, and fix/add some needed data (e.g. device name, protocoll for fritzbox)
        for (idx, d) in enumerate(self.opts.pop("devices", [])):
            _d = {**self.defaults, **d}

            if 'name' not in d:
                _d['name'] = f"device_{ idx }"

            if not _d['hostname'].startswith('https://') and not _d['hostname'].startswith('http://'):
                _d['hostname'] = f"https://{ _d['hostname']}"

            if not _d['username'] or not _d['password']:
                logging.error(f"Username and password are mandatory, device: {_d['name']} ... removed!")
                continue

            try:
                _d['conn'] = Fritzhome(host=_d['hostname'], user=_d['username'], password=_d['password'], ssl_verify=_d['ssl_verify'])
                _d['conn'].login()
            except: # noqa E722
                raise LoginError(_d['username'])

            self.devices.append(_d)

        # TODO #7 - Remove legacy code before releasing v1.2.0
        # top-level connection parameters are deprecated since 1.1.0 and will be removed in 1.2.0
        if 'username' in self.opts or 'password' in self.opts or 'hostname' in self.opts or 'device_types' in self.opts:
            logging.warn('Top-level connection parameters are deprecated and will be removed in version 1.2.0')
            _legacy_device = dict(name='legacy_device', username=self.opts.pop('username', None), password=self.opts.pop('password', None), hostname=self.opts.pop("hostname", "https://fritz.box"), ssl_verify=self.opts.pop('ssl_verify', True), device_types=self.opts.pop('device_types', []))
            try:
                _legacy_device['conn'] = Fritzhome(host=_legacy_device['hostname'], user=_legacy_device['username'], password=_legacy_device['password'], ssl_verify=_legacy_device['ssl_verify'])
                _legacy_device['conn'].login()
            except: # noqa E722
                raise LoginError(_legacy_device['username'])
            self.devices.append(_legacy_device)

    def collect(self):
        """Collect the metrics."""
        for device in self.devices:
            smart_devices = device['conn'].get_devices()

            # thermostats
            for _device in smart_devices:
                dev = dict(
                    fb_name=device['name'],
                    ain=_device.ain,
                    device=_device.name,
                    manufacturer=_device.manufacturer,
                    type=_device.productname,
                    has_thermostat=str(_device.has_thermostat),
                    has_temperature_sendor=str(_device.has_temperature_sensor),
                    has_switch=str(_device.has_switch)
                )
                fb_dev_info = InfoMetricFamily('p3e_fb_temperator_sensor', 'FritzBox device information')
                fb_dev_info.add_metric(labels=dev.keys(), value=dev)
                yield fb_dev_info

                if 'temperature_sensor' in device['device_types'] or device['device_types'] == [] and _device.has_temperature_sensor:
                    fb_temp_gauge = GaugeMetricFamily('p3e_fb_temperatur_sensor', 'Current and target temperature data', labels=['ain', 'device', 'fb_name', 'temperature'])
                    fb_temp_gauge.add_metric([_device.ain, _device.name, dev['fb_name'], 'actual'], _device.actual_temperature)
                    fb_temp_gauge.add_metric([_device.ain, _device.name, dev['fb_name'], 'comfort'], _device.comfort_temperature)
                    fb_temp_gauge.add_metric([_device.ain, _device.name, dev['fb_name'], 'eco'], _device.eco_temperature)
                    yield fb_temp_gauge

                if hasattr(_device, 'battery_level') and hasattr(_device, 'battery_low'):
                    fb_battery_gauge = GaugeMetricFamily('p3e_fb_battery_status', 'Battery level and status', labels=['ain', 'device', 'fb_name', 'battery_low'])
                    fb_battery_gauge.add_metric([_device.ain, _device.name, dev['fb_name'], str(_device.battery_low)], _device.battery_level)
                    yield fb_battery_gauge
