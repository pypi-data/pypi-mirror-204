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
    'version': '0.1.1',
    'description': 'Displays os info based on /etc/os-release',
    'long_description': '# OSRI: OS Release Info\n\nA CLI that shows parsed data from an linux os release file, usually located at /etc/os-release.\n\n## Installation\n\nInstall from a git branch:\n\n```sh\npip install git+https://github.com/odra/osri.git@master\n```\n\n## Usage\n\nShowing the CLI version:\n\n```sh\nosri version\n```\n\nDisplaying an os release info (path defaults to `/etc/os-release`):\n\n```sh\nosri display\nosri display --path /etc/another-os-release\n```\n\n## License\n\n[MIT](./LICENSE)\n',
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
