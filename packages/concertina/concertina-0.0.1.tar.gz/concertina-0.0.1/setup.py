# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['concertina']

package_data = \
{'': ['*']}

install_requires = \
['musthe>=1.0.0,<2.0.0', 'pydantic>=1.10.2,<2.0.0', 'rich>=12.6.0,<13.0.0']

setup_kwargs = {
    'name': 'concertina',
    'version': '0.0.1',
    'description': '',
    'long_description': '',
    'author': 'Ryan J. Miller',
    'author_email': 'rjmiller10@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
