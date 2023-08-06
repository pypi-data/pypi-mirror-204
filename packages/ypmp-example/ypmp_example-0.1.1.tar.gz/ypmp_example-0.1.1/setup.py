# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ypmp_example']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ypmp-example',
    'version': '0.1.1',
    'description': 'Example package for YP 24',
    'long_description': 'None',
    'author': 'ovsds',
    'author_email': 'ovsds@yandex-team.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
