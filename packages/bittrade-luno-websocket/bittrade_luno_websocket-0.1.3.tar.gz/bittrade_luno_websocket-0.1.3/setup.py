# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bittrade_luno_websocket',
 'bittrade_luno_websocket.channels',
 'bittrade_luno_websocket.connection',
 'bittrade_luno_websocket.models',
 'bittrade_luno_websocket.models.rest',
 'bittrade_luno_websocket.rest',
 'bittrade_luno_websocket.signing']

package_data = \
{'': ['*']}

install_requires = \
['ccxt>=2.7.91,<3.0.0',
 'elm-framework-helpers>=0.2.6,<0.3.0',
 'orjson>=3.8.6,<4.0.0',
 'reactivex>=4.0.4,<5.0.0',
 'requests>=2.28.2,<3.0.0',
 'returns>=0.19.0,<0.20.0',
 'websocket-client>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'bittrade-luno-websocket',
    'version': '0.1.3',
    'description': '',
    'long_description': '',
    'author': 'Matt',
    'author_email': 'matt@techspace.asia',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
