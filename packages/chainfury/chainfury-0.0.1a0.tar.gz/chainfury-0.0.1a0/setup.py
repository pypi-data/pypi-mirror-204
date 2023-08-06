# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chainfury']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chainfury',
    'version': '0.0.1a0',
    'description': 'ChainFury from NimbleBox',
    'long_description': '# ChainFury\n',
    'author': 'Yash Bonde',
    'author_email': 'yash@nimblebox.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
