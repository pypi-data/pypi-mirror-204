# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiopinecone', 'aiopinecone.schemas']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0',
 'pydantic>=1.10.7,<2.0.0',
 'typing-extensions>=4.5.0,<5.0.0']

setup_kwargs = {
    'name': 'aiopinecone',
    'version': '0.1.2',
    'description': 'An asyncio-compatible client for Pinecone DB',
    'long_description': '# aiopinecone\nAn asynchronous Pinecone DB Client, completely unaffiliated with Pinecone or Pinecone Systems, Inc.\n',
    'author': 'Nikhil Shinday',
    'author_email': 'nikhil@buildbetter.app',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
