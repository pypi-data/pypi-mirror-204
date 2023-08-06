# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['compas_lcmtypes',
 'compas_lcmtypes.geolcm',
 'compas_lcmtypes.navlcm',
 'compas_lcmtypes.senlcm',
 'compas_lcmtypes.stdlcm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'compas-lcmtypes',
    'version': '0.1.0',
    'description': 'CoMPAS LCM types',
    'long_description': 'None',
    'author': 'Kevin Barnard',
    'author_email': 'kbarnard@mbari.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
