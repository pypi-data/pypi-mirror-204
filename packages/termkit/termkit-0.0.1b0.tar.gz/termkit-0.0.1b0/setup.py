# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['termkit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'termkit',
    'version': '0.0.1b0',
    'description': 'Command Line Tools with ease',
    'long_description': '# termkit\nCommand Line Tools with ease\n',
    'author': 'Thomas Mahé',
    'author_email': 'contact@tmahe.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
