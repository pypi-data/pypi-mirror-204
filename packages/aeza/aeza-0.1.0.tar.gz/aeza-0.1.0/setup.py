# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aeza']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aeza',
    'version': '0.1.0',
    'description': 'Aeza.net official API (name occupy package)',
    'long_description': '# aeza\n\nЭтот пакет создан, для того чтобы занять название aeza в pypi.org. Он принадлежит проекту [aeza.net](https://aeza.net/).\n\nThis package is created to occupy the name aeza in pypi.org. It belongs to the [aeza.net](https://aeza.net/) project\n',
    'author': 'Egor Ternovoy',
    'author_email': 'cofob@riseup.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
