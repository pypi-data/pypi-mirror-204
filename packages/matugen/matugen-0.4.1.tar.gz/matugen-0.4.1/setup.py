# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matugen']

package_data = \
{'': ['*']}

install_requires = \
['material-color-utilities-python==0.1.5', 'rich>=12.5.1,<13.0.0']

entry_points = \
{'console_scripts': ['matugen = matugen.__main__:main']}

setup_kwargs = {
    'name': 'matugen',
    'version': '0.4.1',
    'description': '',
    'long_description': '<div align="center">\n     <img src="https://user-images.githubusercontent.com/81521595/226138807-db504bdf-4eb5-4fe9-9ee5-a1a1395d70dc.png" width=140>\n      <h1>Matugen</h1>\n </div>\n    \n<div align="center">\n  <b>A material you color generation tool for linux</b>\n</div>\n\n<div align="center">\n    <a href="#installation">Installation</a>\n    ·\n    <a href="#usage">Usage</a>\n    ·\n    <a href="https://github.com/InioX/matugen/wiki">Wiki</a>\n</div>\n\n<div align="center">\n     <br>\n     <a href="https://pypi.org/project/matugen/">\n          <img alt="PyPI" src="https://img.shields.io/pypi/v/matugen?color=white&logo=pypi&logoColor=white&style=for-the-badge">\n     </a>\n     <a href="https://github.com/InioX/Matugen/actions/workflows/python-app.yml">\n          <img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/InioX/matugen/python-app.yml?color=white&style=for-the-badge">\n     </a>\n     <a href="https://github.com/InioX/matugen/tags/">\n          <img alt="GitHub tag (latest by date)" src="https://img.shields.io/github/v/tag/InioX/matugen?color=white&logo=github&logoColor=white&style=for-the-badge">\n     </a>\n</div>\n\n## Description\n[Material Design 3](https://m3.material.io/) offers a new color system that allows for more flexible and dynamic use of color. The new system includes a wider range of colors, as well as a range of tints and shades that can be used to create subtle variations in color.\n\n## Installation\n### From Pypi\n>**Note** Assuming you have python with pip installed\n```shell\npip install matugen\n```\n\n### Usage\n```shell\n# Dark theme\nmatugen /path/to/wallpaper/\n# Light theme\nmatugen /path/to/wallpaper/ -l\n```\nExample:\n```shell\nmatugen ~/wall/snow.png -l\n```\n\n### From repo with poetry\n>**Note** Assuming you already have [Poetry](https://python-poetry.org/) installed:\n```shell\ngit clone https://github.com/InioX/matugen && cd matugen\npoetry install\n```\n\n#### Usage\n```shell\n# Dark theme\npoetry run matugen /path/to/wallpaper/\n# Light theme\npoetry run matugen /path/to/wallpaper/ -l\n```\nExample:\n```shell\npoetry run matugen ~/wall/snow.png -l\n```\n\n## Showcase\nShowcase with Hyprland, Waybar, kitty, and fish shell:\n\n>**Warning**\n>The preview and usage may be outdated.\n\n[![](https://markdown-videos.deta.dev/youtube/rMxoORO41rs)](https://youtu.be/rMxoORO41rs)\n',
    'author': 'InioX',
    'author_email': 'justimnix@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
