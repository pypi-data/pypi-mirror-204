# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['awesom']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.1,<4.0.0', 'numpy>=1.23.4,<2.0.0', 'scipy>=1.9.3,<2.0.0']

setup_kwargs = {
    'name': 'awesom',
    'version': '0.1.4',
    'description': 'Self-organizing map framework for Python',
    'long_description': '[![mypy](https://github.com/Teagum/blossom/actions/workflows/mypy.yml/badge.svg)](https://github.com/Teagum/blossom/actions/workflows/mypy.yml)\n[![pylint](https://github.com/Teagum/blossom/actions/workflows/pylint.yml/badge.svg)](https://github.com/Teagum/blossom/actions/workflows/pylint.yml)\n\n# Awesom\nSelf-organizing map framework for Python\n\n\n```python\nimport matplotlib.pyplot as plt\n\nfrom awesom import datasets\nfrom awesom import plot as asp\nfrom awesom.som import IncrementalMap\n\n\nX, y = datasets.norm_circle(5, 500, 1, radius=4)\n\nsom = IncrementalMap((7, 7, X.shape[1]), 100, 0.04, 4)\nsom.fit(X)\n\nfig, ax = plt.subplots(1, 1)\nasp.data_2d(ax, X, y)\nasp.wire(ax, som)\n```\n\n![SOM wire plot](https://user-images.githubusercontent.com/11088297/209104159-958cfbef-15f5-4259-9c15-bfebcb76058e.png "Input dataspce with wire plot")\n',
    'author': 'Michael Blaß',
    'author_email': 'mblass@posteo.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Teagum/awesom',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
