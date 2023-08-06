# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vaxa_plotly_branding']

package_data = \
{'': ['*']}

install_requires = \
['pillow>=9.5.0,<10.0.0', 'plotly>=5.13.1,<6.0.0']

setup_kwargs = {
    'name': 'vaxa-plotly-branding',
    'version': '0.1.2',
    'description': '',
    'long_description': 'Automatically brands Plotly charts with Vaxa Analytics branding.',
    'author': 'Curtis West',
    'author_email': 'curtis@curtiswest.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
