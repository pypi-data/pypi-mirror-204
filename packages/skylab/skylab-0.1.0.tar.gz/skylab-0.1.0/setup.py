# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skylab']

package_data = \
{'': ['*'], 'skylab': ['css/*']}

install_requires = \
['pydantic>=1.10.7,<2.0.0',
 'pytest>=7.3.1,<8.0.0',
 'requests>=2.28.2,<3.0.0',
 'textual[dev]>=0.19.1,<0.20.0',
 'tzlocal>=4.3,<5.0']

entry_points = \
{'console_scripts': ['skylab = skylab.__main__:main']}

setup_kwargs = {
    'name': 'skylab',
    'version': '0.1.0',
    'description': 'A TUI for showing latest upcomming rocket launches.',
    'long_description': '',
    'author': 'SerhiiStets',
    'author_email': 'stets.serhii@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
