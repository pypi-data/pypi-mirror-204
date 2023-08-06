# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.aio_spamwatch']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7']

setup_kwargs = {
    'name': 'aio-spamwatch',
    'version': '0.0.5',
    'description': 'An asynchronous Python wrapper for the SpamWatch API.',
    'long_description': '<h1 assign="center">aio-spamwatch<h1>\n\n[![PyPI version](https://img.shields.io/pypi/v/aio-spamwatch.svg)](https://pypi.org/project/aio-spamwatch/)\n[![License](https://img.shields.io/github/license/NachABR/aio-spamwatch.svg)](https://github.com/NachABR/aio-spamwatch/blob/master/LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nAn asynchronous Python wrapper for the [SpamWatch API](https://spamwat.ch/).\n\n## Installation\n\n```bash\npip install aio-spamwatch\n```\n\n## Usage\n```python\nimport asyncio\nfrom aio_spamwatch import SpamwatchAPI\n\nclient = SpamwatchAPI(token="TOKEN_HERE")\n\n\nasync def main():\n    # import aiohttp\n    # client = SpamwatchAPI(token="TOKEN_HERE", session=aiohttp.ClientSession())\n    version = await client.version()\n    print(version)\n\n\nasyncio.run(main())\n```\n\n\n',
    'author': 'NachABR',
    'author_email': 'nachabr@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
