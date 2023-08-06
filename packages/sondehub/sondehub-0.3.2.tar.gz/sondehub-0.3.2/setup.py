# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sondehub']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.44,<2.0.0',
 'paho-mqtt>=1.5.1,<2.0.0',
 'python-dateutil>=2.8,<3.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['sondehub = sondehub:__main__.main']}

setup_kwargs = {
    'name': 'sondehub',
    'version': '0.3.2',
    'description': 'SDK to access SondeHub open data, and helpers for uploading telemetry.',
    'long_description': '# SondeHub (and SondeHub-Amateur) Python Library\n\nThis repository contains:\n* A uploader class for submitting high-altitude balloon telemetry data to SondeHub-Amateur\n* A simple realtime streaming SDK for the sondehub.org V2 API (both radiosondes, and amateur balloons).\n\n### Contacts\n* [Mark Jessop](https://github.com/darksidelemm) - vk5qi@rfhead.net\n* [Michaela Wheeler](https://github.com/TheSkorm) - radiosonde@michaela.lgbt\n\nYou can often find us in the #highaltitude IRC Channel on Libera Chat.\n\n## Installing\nThis library is available via pypi, and can be installed into your Python environment using:\n```\npip install sondehub\n```\n\n## Submitting Telemetry to SondeHub-Amateur\nA guide on using the SondeHub-Amateur uploader class is available here https://github.com/projecthorus/pysondehub/wiki/SondeHub-Amateur-Uploader-Class-Usage\n\n\n## Streaming Telemetry from Sondehub or Sondehub-Amateur\n\nTo obtain live telemetry from Sondehub, the sondehub class can be used as follows:\n\n```python\nimport sondehub\n\ndef on_message(message):\n    print(message)\n\ntest = sondehub.Stream(on_message=on_message)\nwhile 1:\n    pass\n\n```\n\nThe `on_message` callback will be passed a python dictonary using the [Universal Sonde Telemetry Format](https://github.com/projecthorus/radiosonde_auto_rx/wiki/SondeHub-DB-Universal-Telemetry-Format), or [Amateur Telemetry Format](https://github.com/projecthorus/sondehub-infra/wiki/%5BDRAFT%5D-Amateur-Balloon-Telemetry-Format)\n\n### Filtering\nTo specify a particular serial number, or multiple serial numbers to subscribe to, you can pass these in as a list in the `sondes` argument:\n```python\nimport sondehub\n\ndef on_message(message):\n    print(message)\n\ntest = sondehub.Stream(on_message=on_message, sondes=["R3320848"])\nwhile 1:\n    pass\n\n```\n\nAlternatively, you can add or remove serial numbers from the filter after the stream has started using the `.add_sonde("serial")` and `.remove_sonde("serial")` functions.\ne.g.:\n```\ntest.add_sonde("R3320848")\ntest.remove_sonde("R3320848")\n```\n\n### Amateur Launches\nAmateur balloon launches can be received by subscribing to the `amateur` topic, using the `prefix` argument as follows:\n```\nimport sondehub\n\ndef on_message(message):\n    print(message)\n\ntest = sondehub.Stream(on_message=on_message, prefix="amateur")\n\nwhile 1:\n    pass\n```\n\n## Advanced Usage\n\nManual usage of the Paho MQTT network loop can be obtained by using the `loop`, `loop_forever`, `loop_start` and `loop_stop` functions, taking care to ensure that the different types of network loop aren\'t mixed. See Paho documentation [here](https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php#network-loop).\n\n```python\ntest = sondehub.Stream(on_message=on_message, sondes=sondes, auto_start_loop=False)\ntest.loop_forever()\n```\n\n### CLI Usage\n#### Live streaming data\n```sh\n# all radiosondes\nsondehub\n# single radiosonde\nsondehub --serial "IMET-73217972"\n# multiple radiosondes\nsondehub --serial "IMET-73217972" --serial "IMET-73217973"\n#pipe in jq\nsondehub | jq .\n{\n  "subtype": "SondehubV1",\n  "temp": "-4.0",\n  "manufacturer": "SondehubV1",\n  "serial": "IMET54-55067143",\n  "lat": "-25.95437",\n  "frame": "85436",\n  "datetime": "2021-02-01T23:43:57.043655Z",\n  "software_name": "SondehubV1",\n  "humidity": "97.8",\n  "alt": "5839",\n  "vel_h": "-9999.0",\n  "uploader_callsign": "ZS6TVB",\n  "lon": "28.19082",\n  "software_version": "SondehubV1",\n  "type": "SondehubV1",\n  "time_received": "2021-02-01T23:43:57.043655Z",\n  "position": "-25.95437,28.19082"\n}\n....\n\n```\n\nFor amateur radiosondes, just append the `--amateur` argument. e.g.:\n\n```\nsondehub --amateur\n```\n\n\n## Downloading Archived Radiosonde Telemetry Data\nArchived radiosonde telemetry data (Meteorological Radiosondes only) can be downloaded from our S3 bucket using:\n```\nsondehub --download S2810113\n```\n\n\n## Open Data Access\n\nA basic interface to the Open Data is a available using `sondehub.download(serial=, datetime_prefix=)`. When using datetime_prefix only summary data is provided (the oldest, newest and highest frames)\n\n```\nimport sondehub\nframes = sondehub.download(datetime_prefix="2018/10/01")\nframes = sondehub.download(serial="serial")\n```\n\n## Data license\n\nData is provided under the [Creative Commons BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/) license.',
    'author': 'Michaela',
    'author_email': 'git@michaela.lgbt',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/projecthorus/pysondehub',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
