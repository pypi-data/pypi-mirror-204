# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chromat']

package_data = \
{'': ['*']}

install_requires = \
['colorthief>=0.2.1,<0.3.0', 'colour>=0.1.5,<0.2.0', 'rich>=13.3.4,<14.0.0']

setup_kwargs = {
    'name': 'chromat',
    'version': '0.1.0',
    'description': 'color palettes! under heavy construction!',
    'long_description': '\ufeff# chromat: algorithmic color palettes\ncoming soon!\n\nhttps://github.com/hexbenjamin/chromat',
    'author': 'hex benjamin',
    'author_email': 'hex@hexbenjam.in',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/hexbenjamin/chromat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0,<3.11',
}


setup(**setup_kwargs)
