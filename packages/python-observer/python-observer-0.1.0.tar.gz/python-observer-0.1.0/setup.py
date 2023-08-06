# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_observer']

package_data = \
{'': ['*']}

install_requires = \
['humanfriendly>=10.0,<11.0', 'rich>=13.3.4,<14.0.0']

entry_points = \
{'console_scripts': ['observer = python_observer.cli:main']}

setup_kwargs = {
    'name': 'python-observer',
    'version': '0.1.0',
    'description': 'Live reload for Python apps',
    'long_description': None,
    'author': 'Skyascii',
    'author_email': 'savioxavier112@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
