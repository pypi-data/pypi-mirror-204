# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cplighthouse']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cplighthouse',
    'version': '0.0.1',
    'description': '',
    'long_description': '',
    'author': 'Andre Portela',
    'author_email': 'a220102@dac.unicamp.br',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
