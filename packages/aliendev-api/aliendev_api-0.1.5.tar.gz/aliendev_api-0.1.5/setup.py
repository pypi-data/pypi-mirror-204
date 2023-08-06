# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aliendev_api', 'aliendev_api.config']

package_data = \
{'': ['*']}

install_requires = \
['configparser>=5.3.0,<6.0.0',
 'pydantic>=1.10.7,<2.0.0',
 'pymongo>=4.3.3,<5.0.0']

setup_kwargs = {
    'name': 'aliendev-api',
    'version': '0.1.5',
    'description': '',
    'long_description': '',
    'author': 'Nasri Adzlani',
    'author_email': 'nasri@jkt1.ebdesk.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
