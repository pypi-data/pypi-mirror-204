# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['doubt',
 'doubt.datasets',
 'doubt.models',
 'doubt.models.boot',
 'doubt.models.glm',
 'doubt.models.tree']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.2.0,<2.0.0',
 'numpy>=1.23.0,<2.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.4.0,<2.0.0',
 'scikit-learn>=1.1.1,<2.0.0',
 'tables>=3.7.0,<4.0.0',
 'tqdm>=4.62.0,<5.0.0',
 'xlrd>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'doubt',
    'version': '4.4.1',
    'description': 'Bringing back uncertainty to machine learning.',
    'long_description': '# Doubt\n\n*Bringing back uncertainty to machine learning.*\n\n______________________________________________________________________\n[![PyPI Status](https://badge.fury.io/py/doubt.svg)](https://pypi.org/project/doubt/)\n[![Documentation](https://img.shields.io/badge/docs-passing-green)](https://saattrupdan.github.io/doubt/doubt.html)\n[![License](https://img.shields.io/github/license/saattrupdan/doubt)](https://github.com/saattrupdan/doubt/blob/main/LICENSE)\n[![LastCommit](https://img.shields.io/github/last-commit/saattrupdan/doubt)](https://github.com/saattrupdan/doubt/commits/main)\n[![Code Coverage](https://img.shields.io/badge/Coverage-67%25-yellow.svg)](https://github.com/saattrupdan/doubt/tree/dev/tests)\n[![Conference](https://img.shields.io/badge/Conference-AAAI23-blue)](https://arxiv.org/abs/2201.11676)\n\nA Python package to include prediction intervals in the predictions of machine\nlearning models, to quantify their uncertainty.\n\n\n## Installation\n\nIf you do not already have HDF5 installed, then start by installing that. On MacOS this\ncan be done using `sudo port install hdf5` after\n[MacPorts](https://www.macports.org/install.php) have been installed. On Ubuntu you can\nget HDF5 with `sudo apt-get install python-dev python3-dev libhdf5-serial-dev`. After\nthat, you can install `doubt` with `pip`:\n\n```shell\npip install doubt\n```\n\n\n## Features\n\n- Bootstrap wrapper for all Scikit-Learn models\n    - Can also be used to calculate usual bootstrapped statistics of a dataset\n- Quantile Regression for all generalised linear models\n- Quantile Regression Forests\n- A uniform dataset API, with 24 regression datasets and counting\n\n\n## Quick Start\n\nIf you already have a model in Scikit-Learn, then you can simply\nwrap it in a `Boot` to enable predicting with prediction intervals:\n\n```python\n>>> from sklearn.linear_model import LinearRegression\n>>> from doubt import Boot\n>>> from doubt.datasets import PowerPlant\n>>>\n>>> X, y = PowerPlant().split()\n>>> clf = Boot(LinearRegression())\n>>> clf = clf.fit(X, y)\n>>> clf.predict([10, 30, 1000, 50], uncertainty=0.05)\n(481.9203102126274, array([473.43314309, 490.0313962 ]))\n```\n\nAlternatively, you can use one of the standalone models with uncertainty\noutputs. For instance, a `QuantileRegressionForest`:\n\n```python\n>>> from doubt import QuantileRegressionForest as QRF\n>>> from doubt.datasets import Concrete\n>>> import numpy as np\n>>>\n>>> X, y = Concrete().split()\n>>> clf = QRF(max_leaf_nodes=8)\n>>> clf.fit(X, y)\n>>> clf.predict(np.ones(8), uncertainty=0.25)\n(16.933590347847982, array([ 8.93456428, 26.0664534 ]))\n```\n',
    'author': 'Dan Saattrup Nielsen',
    'author_email': 'saattrupdan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/saattrupdan/doubt',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
