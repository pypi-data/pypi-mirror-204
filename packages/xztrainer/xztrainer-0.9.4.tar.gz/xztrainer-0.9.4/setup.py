# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xztrainer', 'xztrainer.logger']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=23.0', 'setuptools>=67.6.0', 'tqdm>=4.62.3']

extras_require = \
{'numpy': ['numpy>=1.24.2'],
 'tensorboard': ['tensorboard>=2.8.0'],
 'torch': ['torch>=1.10.0']}

setup_kwargs = {
    'name': 'xztrainer',
    'version': '0.9.4',
    'description': 'A customizable training pipeline for PyTorch',
    'long_description': 'None',
    'author': 'Maxim Afanasyev',
    'author_email': 'mr.applexz@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
