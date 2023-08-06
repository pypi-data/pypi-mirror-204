# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['myodan_tools', 'myodan_tools.downloader', 'myodan_tools.extractor']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.2.0,<3.0.0',
 'beautifulsoup4>=4.12.2,<5.0.0',
 'lxml>=4.9.2,<5.0.0',
 'numpy>=1.22.2,<2.0.0',
 'replit>=3.2.4,<4.0.0',
 'requests>=2.28.2,<3.0.0',
 'six>=1.16.0,<2.0.0',
 'typer[all]>=0.7.0,<0.8.0',
 'urllib3>=1.26.12,<2.0.0']

entry_points = \
{'console_scripts': ['myodan-tools = myodan_tools.main:app']}

setup_kwargs = {
    'name': 'myodan-tools',
    'version': '0.0.7',
    'description': '',
    'long_description': '# myodan-tools',
    'author': 'Jongho Hong',
    'author_email': 'myodan@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10.0,<3.11',
}


setup(**setup_kwargs)
