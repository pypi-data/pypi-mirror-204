# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daily_leet', 'daily_leet.language_support']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['leetcode = daily_leet.main:app']}

setup_kwargs = {
    'name': 'daily-leet',
    'version': '0.2.7',
    'description': '',
    'long_description': "# `daily-leet`\n\n**Usage**:\n\n```console\n$ daily-leet [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `daily`: Fetch today's daily challenge and create...\n* `new`: Fetch data from a problem's description...\n\n## `daily-leet daily`\n\nFetch today's daily challenge and create files for it, then open the problem page in browser and open the main file in editor\n\n**Usage**:\n\n```console\n$ daily-leet daily [OPTIONS] LANGUAGE:{python|python3|py|cpp|c++|go|golang|rust}\n```\n\n**Arguments**:\n\n* `LANGUAGE:{python|python3|py|cpp|c++|go|golang|rust}`: The language you want to use  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `daily-leet new`\n\nFetch data from a problem's description page and create files for it, then open the problem page in browser and open the main file in editor\n\n**Usage**:\n\n```console\n$ daily-leet new [OPTIONS] LANGUAGE:{python|python3|py|cpp|c++|go|golang|rust}\n```\n\n**Arguments**:\n\n* `LANGUAGE:{python|python3|py|cpp|c++|go|golang|rust}`: The language you want to use  [required]\n\n**Options**:\n\n* `-u, --url TEXT`: The url to fetch data from, usually a problem's description page. e.g. https://leetcode.com/problems/two-sum/. You need to provide either url or problem title.\n* `-t, --title TEXT`: The title of the problem, separated by '-' or ' '. e.g. two-sum. You need to provide either url or problem title.\n* `--help`: Show this message and exit.\n",
    'author': 'madmaxieee',
    'author_email': '76544194+madmaxieee@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
