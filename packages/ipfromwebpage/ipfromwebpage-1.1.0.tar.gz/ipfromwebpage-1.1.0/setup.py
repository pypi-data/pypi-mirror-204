# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipfromwebpage']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.4,<5.0', 'netaddr>=0.8.0,<0.9.0']

entry_points = \
{'console_scripts': ['ipfromwebpage = ipfromwebpage:entrypoint']}

setup_kwargs = {
    'name': 'ipfromwebpage',
    'version': '1.1.0',
    'description': 'Takes a webpage and outputs all ip addresses it finds',
    'long_description': '## ipfromwebpage\n\n[![PyPi](https://img.shields.io/pypi/v/ipfromwebpage.svg)](https://pypi.python.org/pypi/ipfromwebpage)\n[![CircleCI](https://dl.circleci.com/status-badge/img/gh/shepherdjay/ipfromwebpage/tree/master.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/shepherdjay/ipfromwebpage/tree/master)\n[![codecov](https://codecov.io/gh/shepherdjay/ipfromwebpage/branch/master/graph/badge.svg)](https://codecov.io/gh/shepherdjay/ipfromwebpage)\n\n### Summary:\nTakes a webpage and scrapes for IPv4 Addresses. Then prints the IPs. (aggregated where possible)\n\n#### Quickstart:\n\nInstall using `pip install ipfromwebpage`\n\nRun the code as `ipfromwebpage <url>` where `<url>` is the fully qualified URL you wish to scrap for IPs.\n\n#### Code Example:\n```\nipfromwebpage https://www.cloudflare.com/ips\n================\nIPv4 addresses:\n103.21.244.0/22\n103.22.200.0/22\n103.31.4.0/22\n104.16.0.0/12\n108.162.192.0/18\n131.0.72.0/22\n141.101.64.0/18\n162.158.0.0/15\n172.64.0.0/13\n173.245.48.0/20\n188.114.96.0/20\n190.93.240.0/20\n197.234.240.0/22\n198.41.128.0/17\n================\nIPv6 addresses:\n2400:cb00::/32\n2405:8100::/32\n2405:b500::/32\n2606:4700::/32\n2803:f800::/32\n2a06:98c0::/29\n2c0f:f248::/32\n```\n',
    'author': 'Jay Shepherd',
    'author_email': 'shepherdjay@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/shepherdjay/ip-from-webpage',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
