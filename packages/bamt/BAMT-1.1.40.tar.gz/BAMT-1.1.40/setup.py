# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bamt',
 'bamt.external',
 'bamt.external.pyBN',
 'bamt.external.pyBN.classes',
 'bamt.external.pyBN.classes._tests',
 'bamt.external.pyBN.utils',
 'bamt.external.pyBN.utils._tests',
 'bamt.networks',
 'bamt.nodes',
 'bamt.preprocess',
 'bamt.utils']

package_data = \
{'': ['*']}

install_requires = \
['gmr==1.6.2',
 'matplotlib==3.6.2',
 'missingno>=0.5.1,<0.6.0',
 'numpy>=1.24.2',
 'pandas==1.5.2',
 'pgmpy==0.1.20',
 'pomegranate==0.14.8',
 'pyitlib==0.2.2',
 'pyvis>=0.2.1',
 'scikit-learn==1.2.0',
 'scipy>=1.8.0,<2.0.0',
 'setuptools==65.6.3']

setup_kwargs = {
    'name': 'bamt',
    'version': '1.1.40',
    'description': 'data modeling and analysis tool based on Bayesian networks',
    'long_description': ".. image:: /docs/images/BAMT_white_bg.png\n   :align: center\n   :alt: BAMT framework logo\n\n.. start-badges\n.. list-table::\n   :stub-columns: 1\n\n   * - package\n     - | |pypi| |py_8| |py_9| |py_10|\n   * - tests\n     - | |Build| |coverage|\n   * - docs\n     - |docs|\n   * - license\n     - | |license|\n   * - stats\n     - | |downloads_stats| |downloads_monthly| |downloads_weekly|\n\nRepository of a data modeling and analysis tool based on Bayesian networks\n\nBAMT - Bayesian Analytical and Modelling Toolkit. This repository contains a data modeling and analysis tool based on Bayesian networks. It can be divided into two main parts - algorithms for constructing and training Bayesian networks on data and algorithms for applying Bayesian networks for filling gaps, generating synthetic data, assessing edges strength e.t.c.\n\n.. image:: docs/images/bamt_readme_scheme.png\n     :target: docs/images/bamt_readme_scheme.png\n     :align: center\n     :alt: bamt readme scheme\n\nInstallation\n^^^^^^^^^^^^\n\nBAMT package is available via PyPi:\n\n.. code-block:: bash\n\n   pip install bamt\n\nBAMT Features\n^^^^^^^^^^^^^\n\nThe following algorithms for Bayesian Networks learning are implemented:\n\n\n* Building the structure of a Bayesian network based on expert knowledge by directly specifying the structure of the network;\n* Building the structure of a Bayesian network on data using three algorithms - Hill Climbing, evolutionary and PC (evolutionary and PC are currently under development). For Hill Climbing, the following score functions are implemented - MI, K2, BIC, AIC. The algorithms work on both discrete and mixed data.\n* Learning the parameters of distributions in the nodes of the network based on Gaussian distribution and Mixture Gaussian distribution with automatic selection of the number of components.\n* Non-parametric learning of distributions at nodes using classification and regression models.\n* BigBraveBN - algorithm for structural learning of Bayesian networks with a large number of nodes. Tested on networks with up to 500 nodes.\n\nDifference from existing implementations:\n\n\n* Algorithms work on mixed data;\n* Structural learning implements score-functions for mixed data;\n* Parametric learning implements the use of a mixture of Gaussian distributions to approximate continuous distributions;\n* Non-parametric learning of distributions with various user-specified regression and classification models;\n* The algorithm for structural training of large Bayesian networks (> 10 nodes) is based on local training of small networks with their subsequent algorithmic connection.\n\n.. image:: img/BN_gif.gif\n     :target: img/BN_gif.gif\n     :align: center\n     :alt: bn example gif\n\nFor example, in terms of data analysis and modeling using Bayesian networks, a pipeline has been implemented to generate synthetic data by sampling from Bayesian networks.\n\n\n\n.. image:: img/synth_gen.png\n   :target: img/synth_gen.png\n   :align: center\n   :height: 300px\n   :width: 600px\n   :alt: synthetics generation\n\n\nHow to use\n^^^^^^^^^^\n\nThen the necessary classes are imported from the library:\n\n.. code-block:: python\n\n   import bamt.networks as Nets\n\nNext, a network instance is created and training (structure and parameters) is performed:\n\n.. code-block:: python\n\n   bn = Nets.HybridBN(has_logit=False, use_mixture=True)\n   bn.add_edges(discretized_data, scoring_function=('K2',K2Score))\n   bn.fit_parameters(data)\n\n\n\nExamples & Tutorials\n^^^^^^^^^^^^^^^^^^^^^^\n\nMore examples can be found in `tutorials <https://github.com/ITMO-NSS-team/BAMT/tree/master/tutorials>`__  and `Documentation <https://bamt.readthedocs.io/en/latest/examples/learn_save.html>`__.\n\nPublications about BAMT\n^^^^^^^^^^^^^^^^^^^^^^^\n\nWe have published several articles about BAMT:\n\n* `Advanced Approach for Distributions Parameters Learning in Bayesian Networks with Gaussian Mixture Models and Discriminative Models <https://www.mdpi.com/2227-7390/11/2/343>`__ (2023)\n* `BigBraveBN: algorithm of structural learning for bayesian networks with a large number of nodes <https://www.sciencedirect.com/science/article/pii/S1877050922016945>`__ (2022)\n* `MIxBN: Library for learning Bayesian networks from mixed data <https://www.sciencedirect.com/science/article/pii/S1877050921020925>`__ (2021)\n* `Oil and Gas Reservoirs Parameters Analysis Using Mixed Learning of Bayesian Networks <https://link.springer.com/chapter/10.1007/978-3-030-77961-0_33>`__ (2021)\n* `Bayesian Networks-based personal data synthesis <https://dl.acm.org/doi/abs/10.1145/3411170.3411243>`__ (2020)\n\n\nProject structure\n^^^^^^^^^^^^^^^^^\n\nThe latest stable version of the library is available in the master branch.\n\nIt includes the following modules and direcotries:\n\n* `bamt <https://github.com/ITMO-NSS-team/BAMT/tree/master/bamt>`__ - directory with the framework code:\n    * Preprocessing - module for data preprocessing\n    * Networks - module for building and training Bayesian networks\n    * Nodes - module for nodes support of Bayesian networks\n    * Utilities - module for mathematical and graph utilities\n* `data <https://github.com/ITMO-NSS-team/BAMT/tree/master/data>`__  - directory with data for experiments and tests\n* `tests <https://github.com/ITMO-NSS-team/BAMT/tree/master/tests>`__  - directory with unit and integration tests\n* `tutorials <https://github.com/ITMO-NSS-team/BAMT/tree/master/tutorials>`__  - directory with tutorials\n* `docs <https://github.com/ITMO-NSS-team/BAMT/tree/master/docs>`__ - directory with RTD documentation\n\nPreprocessing\n=============\n\nPreprocessor module allows user to transform data according pipeline (similar to pipeline in scikit-learn).\n\nNetworks\n========\n\nThree types of networks are implemented:\n\n* HybridBN - Bayesian network with mixed data\n* DiscreteBN - Bayesian network with discrete data\n* ContinuousBN - Bayesian network with continuous data\n\nThey are inherited from the abstract class BaseNetwork.\n\nNodes\n=====\n\nContains classes for nodes of Bayesian networks.\n\nUtilities\n=========\n\nUtilities module contains mathematical and graph utilities to support the main functionality of the library.\n\n\nWeb-BAMT\n^^^^^^^^\n\nA web interface for BAMT is currently under development.\nThe repository is available at `web-BAMT <https://github.com/aimclub/Web-BAMT>`__\n\nContacts\n^^^^^^^^\n\nIf you have questions or suggestions, you can contact us at the following address: ideeva@itmo.ru (Irina Deeva)\n\nOur resources:\n\n* `Natural Systems Simulation Team <https://itmo-nss-team.github.io/>`__\n* `NSS team Telegram channel <https://t.me/NSS_group>`__\n* `NSS lab YouTube channel <https://www.youtube.com/@nsslab/videos>`__\n\n.. |docs| image:: https://readthedocs.org/projects/bamt/badge/?version=latest\n    :target: https://bamt.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n.. |pypi| image:: https://badge.fury.io/py/bamt.svg\n    :target: https://badge.fury.io/py/bamt\n\n.. |py_10| image:: https://img.shields.io/badge/python_3.10-passing-success\n   :alt: Supported Python Versions\n   :target: https://img.shields.io/badge/python_3.10-passing-success\n\n.. |py_8| image:: https://img.shields.io/badge/python_3.8-passing-success\n   :alt: Supported Python Versions\n   :target: https://img.shields.io/badge/python_3.8-passing-success\n\n.. |py_9| image:: https://img.shields.io/badge/python_3.9-passing-success\n   :alt: Supported Python Versions\n   :target: https://img.shields.io/badge/python_3.9-passing-success\n\n.. |license| image:: https://img.shields.io/github/license/ITMO-NSS-team/BAMT\n   :alt: Supported Python Versions\n   :target: https://github.com/ITMO-NSS-team/BAMT/blob/master/LICENCE\n\n.. |downloads_stats| image:: https://static.pepy.tech/personalized-badge/bamt?period=total&units=international_system&left_color=grey&right_color=blue&left_text=downloads\n :target: https://pepy.tech/project/bamt\n\n.. |downloads_monthly| image:: https://static.pepy.tech/personalized-badge/bamt?period=month&units=international_system&left_color=grey&right_color=blue&left_text=downloads/month\n :target: https://pepy.tech/project/bamt\n\n.. |downloads_weekly| image:: https://static.pepy.tech/personalized-badge/bamt?period=week&units=international_system&left_color=grey&right_color=blue&left_text=downloads/week\n :target: https://pepy.tech/project/bamt\n\n.. |Build| image:: https://github.com/ITMO-NSS-team/BAMT/actions/workflows/bamtcodecov.yml/badge.svg\n   :target: https://github.com/ITMO-NSS-team/BAMT/actions/workflows/bamtcodecov.yml\n\n.. |coverage| image:: https://codecov.io/github/ITMO-NSS-team/BAMT/branch/master/graph/badge.svg?token=9ZX37JNIYZ\n   :target: https://codecov.io/github/ITMO-NSS-team/BAMT\n",
    'author': 'Roman Netrogolov',
    'author_email': 'romius2001@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ITMO-NSS-team/BAMT',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
