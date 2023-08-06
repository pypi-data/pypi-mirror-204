# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['salix_containers', 'salix_containers.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'salix-containers',
    'version': '0.4.1',
    'description': 'Occasionally handy container types',
    'long_description': None,
    'author': 'Salix',
    'author_email': 'salix@pilae.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
