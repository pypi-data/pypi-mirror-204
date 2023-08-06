# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ethereal']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.1.3,<9.0.0',
 'dependency-injector>=4.41.0,<5.0.0',
 'hdwallet>=2.2.1,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'web3>=6.1.0,<7.0.0']

entry_points = \
{'console_scripts': ['ethereal = ethereal:cli']}

setup_kwargs = {
    'name': 'ethereal',
    'version': '0.1.6',
    'description': 'Ergonomic python tooling for web3',
    'long_description': '![Ethereal logo](./docs/images/ethereal_cat.png)\n\n## Ethereal\n\n[![docs](https://readthedocs.org/projects/ethereal/badge/?version=latest)](https://ethereal.readthedocs.io/en/latest/?badge=latest)\n\nEthereal is a lightweight wrapper around the [Web3](https://web3py.readthedocs.io/en/stable/web3.main.html#web3.Web3) class that simplifies\nworking with Ethereum smart contracts.\n\nTo use it, simply create a regular [Web3](https://web3py.readthedocs.io/en/stable/web3.main.html#web3.Web3) instance and write `w3 = Ethereal(w3)`.\nThen, you can use w3 as usual, but with additional methods\naccessible under the `e` property.\n\nFor example, you can call `w3.e.get_abi("0x...")` or\n`w3.e.list_events("0x...", "Mint", "2023-01-01", "2023-02-14")`.\n\nFor more available methods, please refer to the [EtherealFacade](https://ethereal.readthedocs.io/en/latest/?badge=latest#ethereal.facade.EtherealFacade) class.\n\n### Demo\n\n![Ethereal demo](./docs/images/demo.gif)\n\n### Example\n\n```python\nfrom web3.auto import w3\nfrom ethereal import Ethereal\nfrom ethereal import load_provider_from_uri\n\n# If WEB3_PROVIDER_URI env is not set, uncomment the lines below\n# w3 = Web3(load_provider_from_uri("https://alchemy.com/..."))\n\nw3 = Ethereal(w3)\n\nADDRESS = "0xB0B195aEFA3650A6908f15CdaC7D92F8a5791B0B"\nprint(w3.e.list_events(ADDRESS))\n# Lists event signatures for the contract at ADDRESS\n\nevents = w3.e.get_events(ADDRESS, "Transfer", "2023-01-01", "2023-02-14")\n# Gets all Transfer events for the contract at ADDRESS between 2023-01-01 and 2023-02-14\nprint(events[:10])\n```\n\n### Install\n\n```\npip install ethereal\n```\n\n### Supported networks\n\n- Ethereum\n- Polygon\n- Avalanche\n- Fantom\n- Arbitrum\n- Optimism\n\n### Contributing\n\nFeel free to create feature requests or pull requests :D\n',
    'author': 'Alex Euler',
    'author_email': '0xalexeuler@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
