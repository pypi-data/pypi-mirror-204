# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arc',
 'arc.define',
 'arc.define.param',
 'arc.present',
 'arc.present.markdown',
 'arc.prompt',
 'arc.runtime',
 'arc.types',
 'arc.types.middleware']

package_data = \
{'': ['*']}

install_requires = \
['hypothesis>=6.68.2,<7.0.0']

entry_points = \
{'console_scripts': ['cli = cli:command']}

setup_kwargs = {
    'name': 'arc-cli',
    'version': '8.1.0',
    'description': 'A Regular CLI',
    'long_description': '# ARC: A Regular CLI\nA tool for building declarative, and highly extendable CLI systems for Python 3.9\n\n# ARC Features\n- Command line arguments based on python type hints\n- Arbitrary command nesting\n- Automatic `--help` documentation\n- Fully Extensible with custom middlewares,  types, validators, parameter configurations, etc...\n\n# [Docs](http://arc.seanrcollings.com)\n\n# Quick Start\n\n```py\nimport arc\n\n@arc.command\ndef hello(name: str):\n    """My first arc program!"""\n    arc.arc.print(f"Hello {name}!")\n\nhello()\n```\n\n```\n$ python hello.py Sean\nHello, Sean!\n```\n\n```\n$ python hello.py --help\nUSAGE\n    hello.py [-h] [--] name\n\nDESCRIPTION\n    My first arc program!\n\nARGUMENTS\n    name\n\nOPTIONS\n    --help (-h)  Displays this help message\n```\n\n# Installation\n\n```\n$ pip install arc-cli\n```\n\nClone for development\n```\n$ git clone https://github.com/seanrcollings/arc\n$ poetry install\n```\n\n# Tests\nTests are written with `pytest`\n```\n$ pytest\n```\n',
    'author': 'Sean Collings',
    'author_email': 'seanrcollings@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/seanrcollings/arc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
