# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['compose_x_common',
 'compose_x_common.aws',
 'compose_x_common.aws.ecr',
 'compose_x_common.aws.ecs',
 'compose_x_common.aws.glue']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.22,<2.0', 'flatdict>=4.0.1,<5.0.0', 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'compose-x-common',
    'version': '1.2.12',
    'description': 'Common Library for Compose-X Projects',
    'long_description': '=====================\nCompose-X -- Common\n=====================\n\n\n.. image:: https://img.shields.io/pypi/v/compose_x_common.svg\n    :target: https://pypi.python.org/pypi/compose_x_common\n\n\n--------------------------------------------------------------------------------------\nStandalone library of reusable functions to ease repetitive tasks & AWS functions\n--------------------------------------------------------------------------------------\n\nUsed in a majority of the `Compose-X`_ projects\n\nFeatures\n==========\n\n* Different helpers `compose_x_commom.compose_x_common`\n* Python ARN Regular expressions for different resources `compose_x_commom.aws.arns`\n* AWS Helpers `compose_x_commom.aws`\n\n.. _Compose-X: https://github.com/compose-x\n',
    'author': 'John Preston',
    'author_email': 'john@compose-x.io',
    'maintainer': 'John Preston',
    'maintainer_email': 'john@compose-x.io',
    'url': 'https://github.com/compose-x/compose-x-common-libs/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
