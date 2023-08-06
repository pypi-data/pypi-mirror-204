# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sql_test_kit']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'sql-test-kit',
    'version': '0.1.0',
    'description': 'Framework for testing SQL queries',
    'long_description': '# sql-test-kit\n\nThis is a framework for testing SQL queries',
    'author': 'victorlandeau',
    'author_email': 'vlandeau@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
