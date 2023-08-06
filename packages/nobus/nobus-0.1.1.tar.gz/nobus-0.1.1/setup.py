# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nobus']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nobus',
    'version': '0.1.1',
    'description': '',
    'long_description': '# nobus\n"Nobody But Us" modules for Python\n',
    'author': 'Josh Nobus',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
