# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ultima_scraper_api',
 'ultima_scraper_api.apis',
 'ultima_scraper_api.apis.fansly',
 'ultima_scraper_api.apis.fansly.classes',
 'ultima_scraper_api.apis.fansly.decorators',
 'ultima_scraper_api.apis.onlyfans',
 'ultima_scraper_api.apis.onlyfans.classes',
 'ultima_scraper_api.apis.onlyfans.decorators',
 'ultima_scraper_api.classes',
 'ultima_scraper_api.docs.source',
 'ultima_scraper_api.helpers',
 'ultima_scraper_api.managers',
 'ultima_scraper_api.managers.job_manager',
 'ultima_scraper_api.managers.job_manager.jobs']

package_data = \
{'': ['*'], 'ultima_scraper_api': ['docs/*']}

install_requires = \
['Sphinx>=5.3.0,<6.0.0',
 'aiofiles>=22.1.0,<23.0.0',
 'aiohttp-socks>=0.7.1,<0.8.0',
 'aiohttp>=3.8.4,<4.0.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'dill>=0.3.6,<0.4.0',
 'lxml>=4.9.1,<5.0.0',
 'mergedeep>=1.3.4,<2.0.0',
 'mypy>=0.991,<0.992',
 'orjson>=3.8.3,<4.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-socks[asyncio]==2.2.0',
 'requests[socks]==2.28.2',
 'sphinx-autoapi>=2.0.0,<3.0.0',
 'sphinx-rtd-theme>=1.1.1,<2.0.0',
 'user-agent>=0.1.10,<0.2.0']

extras_require = \
{':sys_platform == "win32"': ['win32-setctime>=1.1.0,<2.0.0']}

setup_kwargs = {
    'name': 'ultima-scraper-api',
    'version': '1.0.5',
    'description': '',
    'long_description': 'None',
    'author': 'DIGITALCRIMINALS',
    'author_email': '89371864+digitalcriminals@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
