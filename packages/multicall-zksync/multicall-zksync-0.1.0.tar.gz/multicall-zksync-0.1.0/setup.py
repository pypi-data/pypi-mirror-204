# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multicall_zksync']

package_data = \
{'': ['*']}

install_requires = \
['eth_retry>=0.1.8,<0.2.0', 'web3>=5.28,<6.0']

setup_kwargs = {
    'name': 'multicall-zksync',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'JIVIN0902',
    'author_email': 'jivinvaidya@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
