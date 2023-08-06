# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['elegantmotd']

package_data = \
{'': ['*']}

install_requires = \
['art>=5.9,<6.0',
 'netifaces>=0.11.0,<0.12.0',
 'psutil>=5.9.5,<6.0.0',
 'rich>=13.3.4,<14.0.0']

entry_points = \
{'console_scripts': ['elegantmotd = elegantmotd.motd:display']}

setup_kwargs = {
    'name': 'elegantmotd',
    'version': '0.2.4',
    'description': 'A visually appealing and informative Message of the Day (MOTD) generator for Linux systems.',
    'long_description': '# ElegantMOTD\n\nElegantMOTD is a Python-based Message of the Day (MOTD) generator for displaying system information in a visually\nappealing and informative manner. It works on Linux systems and provides details such as system load, disk usage, memory\nusage, swap usage, temperature, network interfaces, CPU usage, and more.\n\n## Features\n\n- Rich, colorful text-based output.\n- Displays various system information.\n- Customizable display options.\n- Easy to use and integrate into your system.\n\n## Installation\n- Clone this repository:\n```bash\ngit clone https://github.com/yourusername/elegantmotd.git\ncd elegantmotd\n```\n- Create a virtual environment and activate it:\n\n```bash\npython3 -m venv venv\nsource venv/bin/activate\n```\n\n- Install the required dependencies:\n```bash\npoetry build \n```\n\n## Usage\n\nTo display the Message of the Day, run the following command:\n\n```bash\nelegantmotd\n```\n\n## Output\n\n![Output](resources/output.png)\n\n## Customization\n\nYou can customize the output by modifying the `motd.py` file and adding or removing system information modules as per your preference. The available modules are:\n\n- Load\n- Disk\n- Memory\n- Temperature\n- Process\n- LoggedInUsers\n- Network\n- CPU\n\nTo add or remove a module, simply add or remove the corresponding import statement and the respective class instance from the `sysinfos` list in the `display()` function.\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Emerick Biron',
    'author_email': 'emerick.biron@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/emerick-biron/elegantmotd',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
