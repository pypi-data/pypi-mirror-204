# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skylab']

package_data = \
{'': ['*'], 'skylab': ['css/*']}

install_requires = \
['pydantic>=1.10.7,<2.0.0',
 'pytest-cov>=4.0.0,<5.0.0',
 'pytest>=7.3.1,<8.0.0',
 'requests>=2.28.2,<3.0.0',
 'textual[dev]>=0.19.1,<0.20.0',
 'tzlocal>=4.3,<5.0']

entry_points = \
{'console_scripts': ['skylab = skylab.__main__:main']}

setup_kwargs = {
    'name': 'skylab',
    'version': '0.1.1',
    'description': 'A TUI for showing latest upcoming rocket launches.',
    'long_description': '# Skylab\n\nSkylab is a text user interface (TUI) tool that displays upcoming space launches in a user-friendly way.\n\n## Instalation\n\nTo install Skylab using pip, run the following command:\n\n```\n$ pip install skylab\n```\n\n## Usage\n\nTo use Skylab, simply enter the following command in your terminal:\n\n```\n$ skylab\n```\n\n## Contributing\n\nHelp in testing, development, documentation and other tasks is\nhighly appreciated and useful to the project.\n\nTo get started with developing skylab, see [CONTRIBUTING.md](CONTRIBUTING.md).\n\n## Acknowledgments\n\nThis project makes use of the [The Space Devs API](https://thespacedevs.com/) to retrieve data about upcoming space launches. We would like to thank the creators of this API for providing this valuable service.\n\n## License\n\nSkylab is released under the [MIT License](LICENSE.md).\n',
    'author': 'SerhiiStets',
    'author_email': 'stets.serhii@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/SerhiiStets/skylab',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
