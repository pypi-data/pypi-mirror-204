# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dai_python_commons']

package_data = \
{'': ['*']}

install_requires = \
['boto3-stubs[glue,s3]==1.26.99', 'boto3==1.26.99', 'loguru>=0.6.0,<0.7.0']

extras_require = \
{'data-consolidation': ['pyarrow==7.0.0', 's3fs==0.4.2'],
 'glue': ['awswrangler==3.0.0', 'cryptography==38.0.1']}

setup_kwargs = {
    'name': 'dai-python-commons',
    'version': '4.14.0',
    'description': 'Collection of small python utilities useful for lambda functions or glue jobs. By the Stockholm Public Transport Administration.',
    'long_description': 'None',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
