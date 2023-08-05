# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['experiment_results_manager']

package_data = \
{'': ['*']}

install_requires = \
['fsspec>=2021.4', 'pydantic>=1.6,<2.0']

setup_kwargs = {
    'name': 'experiment-results-manager',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
