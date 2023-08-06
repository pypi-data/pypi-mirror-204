# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['osri']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'prettytable>=3.7.0,<4.0.0']

entry_points = \
{'console_scripts': ['osri = osri.cli:run']}

setup_kwargs = {
    'name': 'osri',
    'version': '0.1.0',
    'description': 'Displays os info based on /etc/os-release',
    'long_description': None,
    'author': 'odra',
    'author_email': 'me@lrossetti.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
