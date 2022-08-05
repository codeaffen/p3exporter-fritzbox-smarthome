"""Module that defines all needed classes and functions for example collector."""
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

        self.username = self.opts.pop("username", "none")
        self.password = self.opts.pop("password", "none")
        self.hostname = self.opts.pop("hostname", "https://fritz.box")
        self.ssl_verify = self.opts.pop("ssl_verify", True)
        self.device_types = self.opts.pop("device_types", [])

        if not self.hostname.startswith('https://') and not self.hostname.startswith('http://'):
            self.hostname = 'https://' + self.hostname

        try:
            self._fritzhome = Fritzhome(host=self.hostname, user=self.username, password=self.password, ssl_verify=self.ssl_verify)
            self._fritzhome.login()
        except: # noqa E722
            raise LoginError(self.username)

    def collect(self):
        """Collect the metrics."""
        devices = self._fritzhome.get_devices()

        # thermostats
        if 'temperature_sensor' in self.device_types or self.device_types == []:
            for _device in devices:
                if _device.has_temperature_sensor:
                    dev = {'ain': _device.ain, 'device': _device.name, 'type': _device.productname, 'has_thermostat': str(_device.has_thermostat)}
                    fb_dev_info = InfoMetricFamily('p3e_fb_temperator_sensor', 'FritzBox device information')
                    fb_dev_info.add_metric(labels=dev.keys(), value=dev)
                    yield fb_dev_info

                    fb_dev_gauge = GaugeMetricFamily('p3e_fb_temperatur_sensor', 'Current temperature', labels=['ain', 'device', 'temperature'])
                    fb_dev_gauge.add_metric([_device.ain, _device.name, 'actual'], _device.actual_temperature)
                    fb_dev_gauge.add_metric([_device.ain, _device.name, 'comfort'], _device.comfort_temperature)
                    fb_dev_gauge.add_metric([_device.ain, _device.name, 'eco'], _device.eco_temperature)
                    yield fb_dev_gauge
