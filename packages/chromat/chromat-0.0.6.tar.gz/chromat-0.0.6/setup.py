# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chromat', 'chromat.palette', 'chromat.swatch', 'chromat.utility']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.2.0,<3.0.0',
 'numpy>=1.22.2,<2.0.0',
 'replit>=3.2.4,<4.0.0',
 'rich>=13.3.4,<14.0.0',
 'urllib3>=1.26.12,<2.0.0']

setup_kwargs = {
    'name': 'chromat',
    'version': '0.0.6',
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
