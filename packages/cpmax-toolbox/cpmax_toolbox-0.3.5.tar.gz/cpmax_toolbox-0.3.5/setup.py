# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cpmax_toolbox']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.0,<4.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pytz>=2022.7.1,<2023.0.0',
 'requests>=2.28.2,<3.0.0',
 'rich>=13.3.1,<14.0.0',
 'scipy>=1.10.1,<2.0.0']

setup_kwargs = {
    'name': 'cpmax-toolbox',
    'version': '0.3.5',
    'description': '',
    'long_description': '',
    'author': 'JRoseCPMax',
    'author_email': 'j.rose@cpmax.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
