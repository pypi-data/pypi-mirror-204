# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crispr_library_prep']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.81,<2.0',
 'matplotlib>=3.7.1,<4.0.0',
 'numpy>=1.23,<2.0',
 'pandas>=1.5.3,<2.0.0',
 'scipy>=1.10.1,<2.0.0',
 'typeguard>=3.0.2,<4.0.0']

setup_kwargs = {
    'name': 'crispr-library-prep',
    'version': '0.1.9',
    'description': '',
    'long_description': '',
    'author': 'Basheer Becerra',
    'author_email': 'bbecerr@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
