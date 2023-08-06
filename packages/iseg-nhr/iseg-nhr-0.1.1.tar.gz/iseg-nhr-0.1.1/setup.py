# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iseg_nhr']

package_data = \
{'': ['*']}

install_requires = \
['PyVISA>=1.13.0,<2.0.0']

setup_kwargs = {
    'name': 'iseg-nhr',
    'version': '0.1.1',
    'description': 'Python interface for an ISEG NHR high-voltage power supply',
    'long_description': '# iseg-nhr\n[![Python versions on PyPI](https://img.shields.io/pypi/pyversions/iseg-nhr.svg)](https://pypi.python.org/pypi/iseg-nhr/)\n[![iseg-nhr version on PyPI](https://img.shields.io/pypi/v/iseg-nhr.svg "iseg-nhr on PyPI")](https://pypi.python.org/pypi/iseg-nhr/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nPython interface for an ISEG NHR high-voltage power supply\n\n## Example\n```Python\nfrom iseg_nhr import NHR, Polarity\n\npsu = NHR("COM3")\n\npolarity = psu.channel0.voltage.polarity\nprint(polarity)\n\npsu.channel0.voltage.setpoint = 1_000\npsu.channel0.on()\nprint(psu.channel0.voltage.measured)\nprint(psu.channel0.current.measured)\n```\n\n## Implementation\nThe main NHR class has the following attributes and methods:  \n`NHR`\n* `channel{i}`  \n  `Channel` class specifying all options for a specific channel\n* `supply`  \n  `Supply` class containing the supply voltages \n* `identity`  \n  *IDN?; model, serial number etc.\n* `status_clear()`  \n  *CLS\n* `reset`  \n  *RST\n* `operation_complete`  \n  *OPC\n* `instruction_set`  \n  instruction set used by the module\n* `lockout()`  \n  Disable local control of the module\n* `local()`  \n  Enable local control of the module\n* `control_register`  \n  module control register \n* `status_register`  \n  module status register\n* `event_register`  \n  module event register\n* `event_clear()`  \n  clear the module event register\n* `temperature`  \n  module temperature\n* `number_channels`  \n  number of module channels\n* `firmware_version`  \n  firmware version\n* `firmware_release`  \n  firmware release date\n* `config`  \n  config mode, either normal or configuration mode\n* `config_save`  \n  save current configuration\n* `voltages`  \n  return the measured voltage of each channel\n* `currents`  \n  return the measured current of each channel\n* `setpoints`  \n  return the setpoint voltage of each channel\n* `on([0,1])`  \n  turn on channels 0 and 1\n* `off([0,1])`  \n  turn off channels 0 and 1\n\n`Channel`\n* `voltage`  \n  `Voltage` class\n* `current`  \n  `Current` class\n* `on_state`  \n  boolean for on state of channel\n* `on()`  \n  turn channel on\n* `off()`  \n  turn channel off\n* `emergency_off()`  \n  turn channel off immidiately, ignoring ramp settings\n* `emergency`  \n  boolean for channel emergency\n* `emergency_clear`  \n  clear channel emergency\n* `event_clear()`  \n  clear channel events\n* `control_register`  \n  channel control register\n* `status_register`  \n  channel status register\n* `event_register`  \n  channel event register\n* `polarity`  \n  channel polarity\n* `polarity_list`  \n  list of channel polarity options\n* `output_mode`  \n  channel output mode\n* `output_mode_list`  \n  channel output mode options\n* `inhibit`  \n  channel inhibit setting\n* `inhibit_options`  \n  channel inhibit options\n\n`Voltage`\n* `ramp`  \n  `Ramp` class\n* `measured`  \n  measured output voltage\n* `setpoint`  \n  voltage setpoint\n* `limit`  \n  voltage limit\n* `maximum`  \n  nominal output voltage\n* `maximum`  \n  voltage mode with polarity sign\n* `mode_list`  \n  voltage mode options\n* `bounds`  \n  output voltage bounds\n\n`Current` has the same attributes and methods, excluding the setpoint\n\n`Ramp`\n* `speed`  \n  ramp speed in unit/s\n* `speed_up`  \n  upward ramp speed in unit/s\n* `speed_down`  \n  downward ramp speed in unit/s\n* `speed_min`  \n  minimum ramp speed in unit/s\n* `speed_max`\n  maximum ramp speed in unit/s',
    'author': 'ograsdijk',
    'author_email': 'o.grasdijk@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ograsdijk/iseg-nhr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
