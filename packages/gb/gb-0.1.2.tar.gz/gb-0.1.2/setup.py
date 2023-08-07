# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gb']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0,<9.0', 'python-magic>=0.4.27,<0.5.0', 'tornado>=6.0,<7.0']

entry_points = \
{'console_scripts': ['gb = gb.__main__:main']}

setup_kwargs = {
    'name': 'gb',
    'version': '0.1.2',
    'description': 'A Python gopher server.',
    'long_description': '![gb logo, a gopher in a ball](https://src.tty.cat/supakeen/gb/raw/branch/master/doc/_static/logo-doc.png)\n\n# gb\n\n![rtd badge](https://readthedocs.org/projects/gb/badge/?version=latest) ![license badge](https://gb.readthedocs.io/en/latest/_static/license.svg) ![black badge](https://img.shields.io/badge/code%20style-black-000000.svg)\n\n## About\n\n`gb` or gopherball is a gopher server written in Python with the main goals of\nease of use and integration. The name gopherball is inspired by a recurring\ntheme in the Calvin & Hobbes comicbooks and a tongue in cheek reference of an\nalternative to the World Wide Web as we know it today.\n\n## Examples\nQuick examples to get you running.\n\n`gb --mode=implicit .` will start a gopher server on `127.0.0.1` port `7070` serving\na recursive index of files starting from the current directory.\n\n`gb --mode=implicit --magic .` will start `gb` in magic-mode on `127.0.0.1` port\n`7070`. Magic mode will make `gb` guess at filetypes.\n\n`gb --mode=implicit --host="127.1.1.1" --port 1025 .` will start `gb` in implicit\nmode on the chosen ip and port. Note that using ports under 1024 requires\nsuperuser permissions!\n\n## Technology\n`gb` is written with the help of Python 3.9 and higher and the Tornado\nframework for its networking.\n\n## Modes\n`gb` has one main mode of operation that is commonly used. More modes are\nplanned for the future.\n\n### implicit\nImplicit mode serves a directory recursively. Indexes are automatically\ngenerated and text files are served to the client. Data files are also\nsupported.\n\n## Magic\n`gb` will serve all non-directories as type 9 files, these are non-readable\nfiles and most clients will prompt for download. Turning on magic with\n`--magic` will let `gb` try to determine the correct filetypes.\n\n## Contributing\nThe source code for `gb` lives on my Gitea where you can also submit issues and\npull requests. It mostly needs help by people with the ability to test in\nvarious clients and libraries that might still support the gopher protocol.\n',
    'author': 'Simon de Vlieger',
    'author_email': 'cmdr@supakeen.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://src.tty.cat/supakeen/gb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)
