# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spikeometric',
 'spikeometric.datasets',
 'spikeometric.models',
 'spikeometric.stimulus']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.0,<4.0.0',
 'networkx>=3.0,<4.0',
 'numpy>=1.21.4,<2.0.0',
 'scipy>=1.7.3,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'spikeometric',
    'version': '1.0.1',
    'description': 'Spikeometric is a Pytorch Geometric based framework for simulating Spiking Neural Networks using Linear Non-linear Cascade models',
    'long_description': '# Spikeometric - Linear Non-Linear Cascade Spiking Neural Networks with PyTorch Geometric\n\nThe spikeometric package is a framework for simulating spiking neural networks (SNNs) using generalized linear models (GLMs) and Linear-Nonlinear-Poisson models (LNPs) in Python. It is built on top of the [PyTorch Geometric](https://pytorch-geometric.readthedocs.io/en/latest/) package and makes use of their powerful graph neural network (GNN) modules and efficient graph representation. It is designed to be fast, flexible and easy to use, and is intended for research purposes.\n\n# Install\nBefore installing `spikeometric` you will need to download versions of PyTorch and PyTorch Geometric that work with your hardware. When you have done that (for example in a conda environment), you are ready to download spikeometric with:\n\n    pip install spikeometric\n\n# Documentation\n\nFor more information about the package and a full API reference check out our [documentation](https://spikeometric.readthedocs.io/en/latest/).\n\n# How to contribute\nWe welcome contributions from users and developers. If you find bugs, please report an issue on github.\nIf you would like to contribute to new features you can either find an issue you would like to work on, or fork this project and develop something great. \nSend pull request for review. We will respond as soon as possible.\n',
    'author': 'Jakob Sønstebø',
    'author_email': 'jakobls16@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bioAI-Oslo/Spikeometric',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
