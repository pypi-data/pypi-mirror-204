# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nuvo_serial']

package_data = \
{'': ['*']}

install_requires = \
['icontract>=2.4',
 'pyserial-asyncio>=0.5',
 'pyserial>=3.5',
 'typeguard>=2.10,<3.0']

setup_kwargs = {
    'name': 'nuvo-serial',
    'version': '0.5.2',
    'description': 'Python API implementing the Nuvo Grand Concerto/Essentia G multi-zone audio amplifier serial control protocol',
    'long_description': '# nuvo-serial\nPython API implementing the Nuvo Grand Concerto/Essentia G multi-zone audio amplifier serial control protocol.\n\n\n## Notes\nA [Nuvo Integration](https://github.com/sprocket-9/hacs-nuvo-serial) built using this library, is available to control a Nuvo through a [Home Assistant](https://www.home-assistant.io/) frontend.\n\n## Usage\n\nSupported models: "Grand_Concerto" and "Essentia_G"\n\nasync and sync version of most commands.\n\nCommands return instances of a python dataclass which represents the Nuvo response message type:\n\n```\n* ZoneStatus\n* ZoneConfiguration\n* ZoneVolumeConfiguration\n* ZoneEQStatus\n* ZoneButton\n* ZoneAllOff\n* SourceConfiguration\n* Version\n```\n## Connection\nDirect serial cable or remote network connection using hardware serial-to-network adapter or software such as [ser2net](https://linux.die.net/man/8/ser2net) will\nwork, all that is needed is a change of the port_url argument:\n\nE.g:\n\nLocal: ```/dev/ttyUSB1```\n\nRemote: ```socket://host:port```\n\nA possible ser2net configuration connecting TCP port 10003 to the nuvo device on /dev/ttyUSB1:\n\n```10003:raw:0:/dev/ttyUSB1:57600 8DATABITS NONE 1STOPBIT```\n\n ```port_url="socket://192.168.5.1:10003"```\n\n## Synchronous Interface\n\nNot all the available setter methods are\nshown, but there are methods to configure most fields in each of the data classes.\n\n```python\nfrom nuvo_serial import get_nuvo\n\nnuvo = get_nuvo(port_url=\'/dev/ttyUSB0\', model=\'Grand_Concerto\')\n\nprint(nuvo.get_version()\n# Version(model=\'Grand_Concerto\', product_number=\'NV-I8G\', firmware_version=\'FWv2.66\', hardware_version=\'HWv0\')\n\nprint(nuvo.zone_status(1))\n# ZoneStatus(zone=1, power=True, source=1, volume=20, mute=False, dnd=False, lock=False)\n\nprint(nuvo.zone_configuration(1))\n# ZoneConfiguration(zone=1, enabled=True, name=\'Music Room\', slave_to=0, group=0, sources=[\'SOURCE1\'], exclusive_source=False, ir_enabled=1, dnd=[], locked=False, slave_eq=0)\n\nprint(nuvo.zone_volume_configuration(1))\n# ZoneVolumeConfiguration(zone=1, max_vol=33, ini_vol=20, page_vol=40, party_vol=50, vol_rst=False)\n\nprint(nuvo.zone_eq_status(1))\n# ZoneEQStatus(zone=1, bass=-2, treble=0, loudcmp=True, balance_position=\'C\', balance_value=0)\n\nprint(nuvo.source_configuration(2))\n# SourceConfiguration(source=2, enabled=True, name=\'Sonos\', gain=4, nuvonet_source=False, short_name=\'SON\')\n\n# Turn off zone #1\nprint(nuvo.set_power(1, False))\n# ZoneStatus(zone=1, power=False, source=None, volume=None, mute=None, dnd=None, lock=None)\n\n# Mute zone #1\nnuvo.set_mute(1, True)\n# ZoneStatus(zone=1, power=True, source=1, volume=None, mute=True, dnd=False, lock=False)\n\n# Change Zone name\nprint(nuvo.zone_set_name(1, "Kitchen"))\n# ZoneConfiguration(zone=1, enabled=True, name=\'Kitchen\', slave_to=0, group=0, sources=[\'SOURCE1\'], exclusive_source=False, ir_enabled=1, dnd=[], locked=False, slave_eq=0)\n\n# Change Zone\'s permitted sources\nprint(nuvo.zone_set_source_mask(1, [\'SOURCE3\', \'SOURCE4\']))\nZoneConfiguration(zone=1, enabled=True, name=\'Kitchen\', slave_to=0, group=0, sources=[\'SOURCE3\', \'SOURCE4\'], exclusive_source=False, ir_enabled=1, dnd=[], locked=False, slave_eq=0)\n\n# Change Zone max volume\nprint(nuvo.zone_volume_max(1, 20))\n# ZoneVolumeConfiguration(zone=1, max_vol=20, ini_vol=20, page_vol=40, party_vol=50, vol_rst=False)\n\n# Change Zone Bass\nprint(nuvo.set_bass(1, 6))\n# ZoneEQStatus(zone=1, bass=6, treble=0, loudcmp=True, balance_position=\'C\', balance_value=0)\n\n# Set volume for zone #1\nnuvo.set_volume(1, 15)\n\n# Set source 2 for zone #1 \nnuvo.set_source(1, 2)\n\n# Set balance for zone #1\nnuvo.set_balance(1, L, 8)\n# ZoneEQStatus(zone=1, bass=-2, treble=0, loudcmp=True, balance_position=\'L\', balance_value=8)\n\n```\n\n## Asynchronous Interface\n\nAll the method names and syntax are as above in the sync interface, but now all the methods are coroutines and must\nbe awaited.\n\nAn added feature with the async interface is it will constantly monitor the\nserial line and attempt to classify any messages emitted by the Nuvo.\nA subscriber to these messages in the form of a coroutine callback can optionally be added\nfor any of the Nuvo message data classes.  This allows receiving messages sent\nby the Nuvo in response to commands initiated from Zone keypads.\n\n```python\n\nimport asyncio\nfrom nuvo_serial import get_nuvo_async\n\nasync def message_receiver(message: dict):\n    print(message)\n    # e.g. {\'event_name\': \'ZoneStatus\', \'event\': ZoneStatus(zone=1, power=True, source=1, volume=None, mute=True, dnd=False, lock=False)}\n    # e.g. {\'event_name\': \'ZoneButton\', \'event\': ZoneButton(zone=1, source=1, button=\'PLAYPAUSE\')}\n\nasync def main():\n\n    nuvo = await get_nuvo_async(\'/dev/ttyUSB0\', \'Grand_Concerto\')\n\n    print(await nuvo.zone_status(1))\n    # ZoneStatus(zone=1, power=True, source=1, volume=20, mute=False, dnd=False, lock=False)\n   \n    """message_receiver coro will be called everytime a ZoneStatus message is received\n    from the Nuvo."""\n   nuvo.add_subscriber(message_receiver, "ZoneStatus")\n\n   nuvo.add_subscriber(message_receiver, "ZoneButton")\n   ...\n   nuvo.remove_subscriber(message_receiver, "ZoneStatus")\n   nuvo.disconnect()\n\n\nloop = asyncio.get_event_loop()\nloop.run_until_complete(main())\n\n```\n',
    'author': 'sprocket-9',
    'author_email': 'sprocketnumber9@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sprocket-9/nuvo-serial',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
