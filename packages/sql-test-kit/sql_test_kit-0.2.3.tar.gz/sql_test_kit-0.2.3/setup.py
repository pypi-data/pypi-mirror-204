# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sql_test_kit']

package_data = \
{'': ['*']}

install_requires = \
['db-dtypes[bigquery]>=1.1.1,<2.0.0',
 'google-cloud-bigquery[bigquery]>=3.10.0,<4.0.0',
 'pandas>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'sql-test-kit',
    'version': '0.2.3',
    'description': 'Framework for testing SQL queries',
    'long_description': '# sql-test-kit\n\nThis is a framework for testing SQL queries.\nIt works by directly running the queries against the targeted engine, thus being robust to any change in the\ncorresponding SQL dialect.\nMoreover, it is currently focused on interpolating test data directly inside the SQL queries, making the test much\nquicker than if it were creating temporary tables.\n\n# Application example\n\nYou can find an example in applying the framework to bigquery in the [test_bigquery](tests/test_bigquery.py) file.\n',
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
